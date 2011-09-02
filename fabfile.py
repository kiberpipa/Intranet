#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fabric set of commands for deploying django.

Before sure to provide the following:

* create DB for production and staging according to localsettings.py

"""
# TODO:
# * fix racing conditions (keep state when running bootstrap/deploy)
# * test rollback and backup/restore

# TODO for future:
# * shouldn't be postgres specific
# * date tag backups
# * restore supporting multiple versions, not only latests

import os
import time

from fabric import operations, utils
from fabric.api import run, env, local
from fabric.context_managers import settings, cd, lcd
from fabric.contrib.files import upload_template, exists, sed
from fabric.contrib import django
from fabric.colors import red, green
from fabric.decorators import task, runs_once


# linux
env.user = 'intranet'
# folders/locations
env.home_folder = '/home/%(user)s' % env
env.root_folder = '/home/intranet'
env.staging_folder = os.path.join(env.root_folder, 'staging')
env.staging_media_folder = os.path.join(env.staging_folder, 'media')
env.production_folder = os.path.join(env.root_folder, 'production')
env.production_media_folder = os.path.join(env.production_folder, 'media')
env.backup_folder = os.path.join(env.root_folder, 'backups')
# code
env.repository = 'git://github.com/kiberpipa/Intranet.git'
env.branch = 'deploy'
env.code_folder = os.path.join(env.home_folder, 'code')
# django
env.django_project = 'intranet'
env.production_django_settings = os.path.join(env.root_folder, 'production_localsettings.py')
env.staging_django_settings = os.path.join(env.root_folder, 'staging_localsettings.py')
# django settings
env.PORT = 5432


def install_defaults():
    """Populates sane defaults"""
    # install default buildout
    run('mkdir -p %(home_folder)s/.buildout/{eggs,downloads}' % env)
    run('mkdir -p %(production_folder)s' % env)
    run('mkdir -p %(production_media_folder)s' % env)
    run('mkdir -p %(staging_media_folder)s' % env)
    upload_template('etc/default.cfg.in', '%(home_folder)s/.buildout/default.cfg' % env, env)

    # warn about ssh pub key for -H localhost
    with settings(warn_only=True):
        if run('grep -q -f ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys').return_code != 0:
            operations.abort('%(user)s must be able to run "ssh localhost", please configure .ssh/authorized_keys' % env)

    # warn about localsettings
    for f in [env.staging_django_settings, env.production_django_settings]:
        if not exists(f):
            operations.abort('%s does not exists. Please upload the file and rerun fabric.' % f)

    # prepare code
    if not exists(env.code_folder):
        run('git clone %(repository)s %(code_folder)s -b %(branch)s' % env)


def has_new_commits():
    """Check for fresh deploy branch commits"""
    with lcd(env.code_folder):
        local('git fetch origin')
        output = local('git log %(branch)s...origin/%(branch)s' % env, capture=True)
        if output.strip():
            local('git pull origin')
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

    # strict permissions for settings
    run('chmod 750 %s' % getattr(env, '%s_django_settings' % env.environment))

    # install crontab
    upload_template('etc/crontab.in', '/tmp/intranet.crontab', env)
    run('crontab -l > /tmp/intranet.crontab.old')
    run('crontab < /tmp/intranet.crontab')

    # start supervisord
    run('bin/supervisord')
    time.sleep(15)
    run('bin/supervisorctl status')


@task
def remote_staging_bootstrap(fresh=True):
    """Install and run staging from scratch"""
    env.environment = 'staging'
    if fresh:
        install_defaults()

    # cleanup
    with settings(warn_only=True):
        run('%(staging_folder)s/bin/supervisorctl shutdown' % env)
        run('rm -rf %(staging_folder)s' % env)

    run('mkdir -p %(staging_folder)s' % env)
    with cd(env.staging_folder):
        # TODO: export from /code
        run('git clone %s .' % env.repository)
        run('git checkout %s' % env.branch)
        run('cp etc/buildout.cfg.in buildout.cfg')
        sed('buildout.cfg', '%\(environment\)s', env.environment)
        run('python bootstrap.py')
        run('cp %(staging_django_settings)s %(django_project)s/localsettings.py' % env)
        run('bin/buildout')

        # recreate database
        #run('bin/django')

        if not remote_production_data_restore('staging'):
            run('bin/django syncdb --noinput --traceback --all')
            run('bin/django migrate --fake')
        deploy()


@task
def local_staging_redeploy():
    """Check for new commits and rebootstrap staging"""
    if not has_new_commits():
        return

    with cd(env.code_folder):
        remote_staging_bootstrap(fresh=False)


@task
def remote_staging_redeploy_with_production_data():
    """Production backup and reboostrap staging"""
    remote_production_data_backup()
    with cd(env.code_folder):
        remote_staging_bootstrap(fresh=False)


@task
def remote_production_deploy():
    """Staging to production and rollback on failure"""
    env.environment = 'production'

    env.ver = remote_production_latest_version()
    env.next_ver = env.ver + 1
    is_fresh = env.ver == 0

    with cd(env.production_folder):
        # monkey patch abort function so we just get raised exception
        operations.abort = abort_with_exception
        try:
            if not is_fresh:
                with cd('v%(ver)d' % env):
                    remote_production_data_backup(env.ver)

            run('mkdir v%(next_ver)d' % env)
            with cd('v%(next_ver)d' % env):
                run('cp -R %(staging_folder)s/* .' % env)
                upload_template('etc/buildout.cfg.in', 'buildout.cfg', env)
                run('cp %(production_django_settings)s %(django_project)s/localsettings.py' % env)
                run('bin/buildout -o')

                # everthing went fine.
                if is_fresh:
                    run('bin/django syncdb --noinput --traceback --all')
                    run('bin/django migrate --fake')
                else:
                    run('../v%(ver)d/bin/supervisorctl shutdown' % env)
                run('ln -s ../media media')
                deploy()
        except FabricFailure:
            operations.abort = utils.abort  # unmonkeypatch
            remote_production_rollback()
            print red("Production v%d deploy failed, rollback completed." % env.next_ver)
        else:
            remote_production_data_backup(env.next_ver)
            print green("Successfully deployed production v%d." % env.next_ver)


@runs_once
def remote_production_latest_version():
    """Version number of latest production dir"""
    versions = run('find %(production_folder)s -maxdepth 1 -name "v*"' % env).split() or ['v0']
    latest = sorted(int(os.path.basename(ver).strip('v')) for ver in versions)[-1]
    print "Latest production version: %d" % latest
    return latest


@task
def remote_production_rollback():
    """Clean latest production and deploy previous"""
    env.ver = remote_production_latest_version()
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
            remote_production_data_restore('production', env.prev_ver)
            run('bin/supervisord')
            time.sleep(5)
            run('bin/supervisorctl status')


@task
def local_production_data_backup(backup_location):
    """Backup database and media files"""
    env.backup_location = backup_location

    if not exists(env.backup_location):
        local('mkdir -p %(backup_location)s' % env)

    # backup media files
    local("tar cvfz %(backup_location)s/mediafiles.tar.gz -C media/ ." % env)

    # backup database
    django.project(env.django_project)
    from django.conf import settings
    env.update(settings.DATABASES['default'])

    local('pg_dump -c -p %(PORT)s -U %(USER)s -Fc --no-owner --no-acl -c %(NAME)s -f %(backup_location)s/db.sql' % env)


@task
def remote_production_data_backup(version=None):
    """Backup database and media files"""
    ver_dir = "v%d" % (version or remote_production_latest_version())
    env.backup_location = os.path.join(env.backup_folder, ver_dir)
    env.production_location = os.path.join(env.production_folder, ver_dir)
    return run('cd %(production_location)s && bin/fab local_production_data_backup:%(backup_location)s -H localhost' % env).succeeded


@task
def local_production_data_restore(backup_location):
    """Restore latests database and media files"""
    env.backup_location = backup_location
    if not exists(env.backup_location):
        operations.abort(red("No backup yet: %(backup_location)s" % env, bold=True))

    # restore static files
    local('tar xvfz %(backup_location)s/mediafiles.tar.gz -C media/' % env)

    # restore database
    django.project(env.django_project)
    from django.conf import settings
    env.update(settings.DATABASES['default'])

    local('pg_restore -c -p %(PORT)s -U %(USER)s -Fc --no-acl -e --no-owner -d %(NAME)s %(backup_location)s/db.sql' % env)


@task
def remote_production_data_restore(environment, version=None):
    """Restore latests database and media files"""
    env.ver = version or remote_production_latest_version()
    ver_dir = "v%d" % env.ver
    env.backup_location = os.path.join(env.backup_folder, ver_dir)

    if environment == "staging":
        env.restore_location = env.staging_folder
    elif environment == "production":
        env.restore_location = os.path.join(env.production_folder, ver_dir)
    else:
        operations.abort("unknown '%s' restore environment" % environment)

    with settings(warn_only=True):
        return run('cd %(restore_location)s && bin/fab local_production_data_restore:%(backup_location)s -H localhost' % env).succeeded


class FabricFailure(Exception):
    """Raise this exception instead of sysexit on fabric failure"""


def abort_with_exception(msg):
    raise FabricFailure(msg)
