#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fabric set of commands for deploying django.

Before sure to provide the following:

* create DB for production and staging according to localsettings.py

"""
# TODO:
# * shouldn't be postgres specific

# TODO future:
# * remove ugly hack with symlinking supervisor (probably by patching z3c.recipe.usercrontab)

import os
import time

from fabric import operations, utils
from fabric.api import run, env, local
from fabric.context_managers import settings, cd, lcd
from fabric.contrib.files import upload_template, exists, append, sed
from fabric.contrib import django
from fabric.colors import red, green
from fabric.decorators import task


# linux
env.user = 'intranet'
env.umask = '0027'
# folders/locations
env.home_folder = '/home/%(user)s/' % env
env.root_folder = '/home/intranet/'
env.staging_folder = os.path.join(env.root_folder, 'staging/')
env.production_folder = os.path.join(env.root_folder, 'production/')
env.production_media_folder = os.path.join(env.production_folder, 'media')
env.backup_folder = os.path.join(env.root_folder, 'backups')
# code
env.repository = 'git://github.com/kiberpipa/Intranet.git'
env.branch = 'new_deploy'
# django
env.django_project = 'intranet'
env.production_django_settings = os.path.join(env.root_folder, 'production_localsettings.py')
env.staging_django_settings = os.path.join(env.root_folder, 'staging_localsettings.py')
# django settinsg
env.PORT = 5432


def install_defaults():
    """Populates sane defaults"""
    # install default buildout
    if not exists('%(home_folder)s.buildout/' % env):
        run('mkdir -p %(home_folder)s.buildout/{eggs,downloads}' % env)
    upload_template('buildout.d/default.cfg.in', '%(home_folder)s.buildout/default.cfg' % env, env)

    # set umask
    for f in ['%(home_folder)s/.bashrc', '%(home_folder)s/.bash_profile']:
        append(f % env, 'umask %(umask)s' % env)

    # warn about ssh pub key for -H localhost
    with settings(warn_only=True):
        if run('grep -q -f ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys').return_code != 0:
            operations.abort('%(user)s must be able to run "ssh localhost", please configure .ssh/authorized_keys' % env)

    # warn about localsettings
    for f in [env.staging_django_settings, env.production_django_settings]:
        if not exists(f):
            operations.abort('%s does not exists. Please upload the file and rerun fabric.' % f)


def has_new_commits():
    """Check for fresh deploy branch commits"""
    with lcd(env.staging_folder):
        local('git fetch origin')
        output = local('git log %(branch)s...origin/%(branch)s' % env, capture=True)
    if output.strip():
        print "new commits!"
        return True
    else:
        print "no new commits."
        return False


def deploy():
    """Deploy rutine for Django"""
    run('bin/django syncdb --noinput --traceback --migrate')
    with settings(warn_only=True):
        run('bin/django createinitialrevisions')  # django-revision
        run('bin/django collectstatic --noinput -l')  # staticfiles
    run('bin/supervisord')
    time.sleep(15)
    run('bin/supervisorctl status')


@task
def staging_bootstrap(fresh=True):
    """Install and run staging from scratch"""
    env.environment = 'staging'
    if fresh:
        install_defaults()

    # cleanup
    with settings(warn_only=True):
        run('%(staging_folder)sbin/supervisorctl shutdown' % env)
        run('rm -rf %(staging_folder)s' % env)

    run('mkdir -p %(staging_folder)s' % env)
    with cd(env.staging_folder):
        run('git clone %s .' % env.repository)
        run('git checkout %s' % env.branch)
        run('cp buildout.d/buildout.cfg.in buildout.cfg')
        sed('buildout.cfg', '%\(environment\)s', env.environment)
        run('python bootstrap.py')
        run('cp %(staging_django_settings)s %(django_project)s/localsettings.py' % env)
        run('bin/buildout')
        # TODO: restore if there is backup, fallback to fresh database instead
        if fresh:
            run('bin/django syncdb --noinput --traceback --all')
            run('bin/django migrate --fake')
        else:
            run('bin/fab production_data_restore:staging -H localhost')
        deploy()


@task
def staging_redeploy():
    """Check for new commits and rebootstrap staging"""
    if not has_new_commits():
        return

    staging_bootstrap(fresh=False)


@task
def production_deploy():
    """Staging to production and rollback on failure"""
    env.environment = 'production'
    env.ver = production_latest_version()
    env.next_ver = env.ver + 1
    is_fresh = env.ver == 0
    if not exists(env.production_folder):
        run('mkdir -p %(production_folder)s' % env)
    if not exists(env.production_media_folder):
        run('mkdir %(production_media_folder)s' % env)

    with cd(env.production_folder):
        # monkey patch abort function so we just get raised exception
        operations.abort = abort_with_exception
        try:
            if not is_fresh:
                with cd('v%(ver)d' % env):
                    run('bin/fab production_data_backup -H localhost')

            run('mkdir v%(next_ver)d' % env)
            with cd('v%(next_ver)d' % env):
                run('cp -R %(staging_folder)s* .' % env)
                upload_template('buildout.d/buildout.cfg.in', 'buildout.cfg', env)
                run('cp %(production_django_settings)s %(django_project)s/localsettings.py' % env)
                run('bin/buildout -o')

                # everthing went fine.
                if is_fresh:
                    run('bin/django syncdb --noinput --traceback --all')
                    run('bin/django migrate --fake')
                else:
                    run('../v%(ver)d/bin/supervisorctl shutdown' % env)
                # symlink supervisord for cronjob on startup
                run('ln -f -s bin/supervisord %(root_folder)s/supervisord' % env)
                deploy()
        except FabricFailure:
            operations.abort = utils.abort  # unmonkeypatch
            production_rollback()
            print red("Production v%d deploy failed, rollback completed." % env.next_ver)
        else:
            print green("Successfully deployed production v%d." % env.next_ver)


def production_latest_version():
    """Version number of latest production dir"""
    versions = run('find %(production_folder)s -maxdepth 1 -name "v*"' % env).split() or ['v0']
    latest = sorted(int(os.path.basename(ver).strip('v')) for ver in versions)[-1]
    print "Latest production version: %d" % latest
    return latest


@task
def production_copy_livedata_to_staging():
    """"""
    run('bin/fab production_data_backup -H localhost')
    staging_bootstrap()


@task
def production_rollback():
    """"""
    env.ver = production_latest_version()
    env.prev_ver = env.ver - 1
    print red("Starting rollback...", bold=True)

    with cd(env.production_folder):
        # cleanup
        with settings(warn_only=True):
            run('v%d/bin/supervisorctl shutdown' % env.ver)
        run('rm -rf v%d' % env.ver)

        if env.ver == 1:
            operations.abort('Could not rollback since this is first production deploy.')

        with cd('v%d' % env.prev_ver):
            run('bin/fab production_data_restore:to=production -H localhost')
            run('bin/supervisord')
            time.sleep(5)
            run('bin/supervisorctl status')


@task
def production_data_backup(version=None):
    """Backup database and static files"""
    env.ver = version or production_latest_version()
    ver_dir = "v%d" % env.ver
    env.backup_location = os.path.join(env.backup_folder, ver_dir)
    production = os.path.join(env.production_folder, ver_dir)

    if not exists(env.backup_location):
        local('mkdir -p %(backup_location)s' % env)

    # backup static files
    local('tar cvfz %(backup_location)s/mediafiles.tar.gz -C %(production_media_folder)s .' % env)

    # backup database
    with lcd(production):
        django.project(env.django_project)
        from django.conf import settings
        env.update(settings.DATABASES['default'])

        local('pg_dump -c -p %(PORT)s -U %(USER)s -Fc --no-acl -d %(NAME)s -f %(backup_location)s/db.sql' % env)


@task
def production_data_restore(to):
    """Restore latests database and static files"""
    env.ver = production_latest_version()
    ver_dir = "v%d" % env.ver
    env.backup_location = os.path.join(env.backup_folder, ver_dir)

    if not exists(env.backup_location):
        print red("No backup for production version %d yet." % env.ver, bold=True)
        return

    if to == "staging":
        env.restore_location = env.staging_folder
    elif to == "production":
        env.restore_location = os.path.join(env.production_folder, ver_dir)
    else:
        operations.abort("unknown '%s' restore location" % to)

    # restore static files
    local('tar xvfz %(backup_location)s/mediafiles.tar.gz -C %(production_media_folder)s' % env)

    # restore database
    with lcd(env.restore_location):
        django.project(env.django_project)
        from django.conf import settings
        env.update(settings.DATABASES['default'])

        local('pg_restore -c -p %(PORT)s -U %(USER)s -Fc --no-acl -d %(NAME)s %(backup_location)s/db.sql' % env)


class FabricFailure(Exception):
    """Raise this exception instead of sysexit on fabric failure"""


def abort_with_exception(msg):
    raise FabricFailure(msg)
