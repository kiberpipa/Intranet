#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from fabric.api import run, env, local
from fabric.context_managers import settings, cd, lcd
from fabric.contrib.files import upload_template
from fabric.contrib.files import exists
from fabric import operations, utils


env.user = 'intranet'
env.root_folder = '/home/intranet/'
env.home_folder = '/home/%(user)s/' % env
env.staging_folder = os.path.join(env.root_folder, 'staging/')
env.production_folder = os.path.join(env.root_folder, 'production/')
env.backup_folder = '/var/backups/'
env.staging_django_settings = os.path.join(env.root_folder, 'staging_localsettings.py')
env.production_django_settings = os.path.join(env.root_folder, 'production_localsettings.py')
env.repository = 'git://github.com/kiberpipa/Intranet.git'
env.branch = 'new_deploy'


def install_default_buildout():
    """Populates ~/.buildout/default.cfg"""
    if not exists('%(home_folder)s.buildout/default.cfg' % env):
        run('mkdir -p %(home_folder)s.buildout/{eggs,downloads}' % env)
        upload_template('buildout.d/default.cfg.in', '%(home_folder)s.buildout/default.cfg' % env, env)


def check_for_new_commits():
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
    run('bin/django createinitialrevisions')  # django-revision
    run('bin/supervisord')
    time.sleep(15)
    run('bin/supervisorctl status')


def staging_bootstrap():
    """Install and run staging from scratch"""
    env.environment = 'staging'
    install_default_buildout()
    run('rm -rf %(staging_folder)s' % env)
    run('mkdir -p %(staging_folder)s' % env)
    with cd(env.staging_folder):
        run('git clone %s .' % env.repository)
        run('git checkout %s' % env.branch)
        upload_template('buildout.d/buildout.cfg.in', 'buildout.cfg', env)
        run('python bootstrap.py')
        run('cp %(staging_django_settings)s intranet/localsettings.py' % env)
        run('bin/buildout')
        run('bin/django syncdb --noinput --traceback --all')
        run('bin/django migrate --fake')
        deploy()


def staging_redeploy():
    """Check for update and rebootstrap staging"""
    if not check_for_new_commits():
        return

    with settings(warn_only=True):
        run('%(staging_folder)s/bin/supervisorctl shutdown' % env)

    # TODO: drop database

    staging_bootstrap()


def production_deploy():
    """Staging to production and rollback on failure"""
    env.environment = 'production'
    run('mkdir -p %(production_folder)s' % env)
    env.ver = production_latest_version()
    env.next_ver = env.ver + 1

    with cd(env.production_folder):
        run('mkdir v%(next_ver)d' % env)

        # TODO: do backup

        # monkey patch abort function so we just get raised exception
        operations.abort = abort_with_exception
        try:
            with cd('v%(next_ver)d' % env):
                run('cp -R %(staging_folder)s* .' % env)
                upload_template('buildout.d/buildout.cfg.in', 'buildout.cfg', env)
                run('cp %(production_django_settings)s intranet/localsettings.py' % env)
                run('bin/buildout -o')

                # everthing went fine.
                run('../v%(ver)d/bin/supervisorctl shutdown' % env)
                deploy()
        except FabricFailure:
            operations.abort = utils.abort  # unmonkeypatch
            production_rollback()
            print "Production v%d failed, rollback completed." % env.next_ver
        else:
            print "Production v%d successfully deployed." % env.next_ver


def production_latest_version():
    """Version number of latest production dir"""
    versions = run('find %(production_folder)s -maxdepth 1 -name "v*"' % env).split() or ['v0']
    latest = sorted(int(os.path.basename(ver).strip('v')) for ver in versions)[-1]
    print "Latest production version: %d" % latest
    return latest


def production_copy_livedata_to_staging():
    """"""
    ver = production_latest_version()
    run('cp -r %d/ data/' % ver)
    run('v%d/bin/django dumpdata' % ver)

    # TODO: think through with migrations


def production_rollback():
    """"""
    env.ver = production_latest_version()
    env.prev_ver = env.ver - 1
    with settings(warn_only=True):
        run('v%d/bin/supervisorctl shutdown' % env.ver)

    with cd('v%d' % env.prev_er):
        # TODO: restore backup
        run('bin/supervisord')
        time.sleep(5)
        run('bin/supervisorctl status')

    # cleanup
    run('rm -rf v%d' % env.ver)

# TODO: media files
# TODO: instructions: build-deps, localsettings files, ssh to same user,


class FabricFailure(Exception):
    """Raise this exception instead of sysexit on fabric failure"""


def abort_with_exception(msg):
    raise FabricFailure(msg)
