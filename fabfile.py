#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from fabric.api import run, env, local
from fabric.context_managers import settings, cd


env.user = 'intranet'
env.root_folder = '/home/intranet/'
env.staging_folder = os.path.join(env.root_folder, 'staging/')
env.production_folder = os.path.join(env.root_folder, 'production/')
env.backup_folder = '/var/backups/'
env.staging_django_settings = os.path.join(env.staging_folder, 'staging_localsettings.py')
env.production_django_settings = os.path.join(env.staging_folder, 'production_localsettings.py')
env.repository = 'git://github.com/kiberpipa/Intranet.git'
env.branch = 'deploy'


def check_for_new_commits():
    """Check for fresh deploy branch commits"""
    local('git fetch origin')
    output = local('git log %(deploy)s...origin/%(deploy)s')
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
    time.sleep(5)
    run('bin/supervisorctl status')
    return True


def staging_bootstrap():
    """Install and run staging from scratch"""
    run('mkdir -p %(staging_folder)s' % env)
    with cd(env.staging_folder):
        run('git clone %s .' % env.repository)
        run('git checkout %s' % env.branch)
        run('ln -s buildout.d/staging.cfg buildout.cfg')
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

    # delete current staging
    run('rm -rf %(stagging_folder)s' % env)

    staging_bootstrap()


def production_deploy():
    """Staging to production and rollback on failure"""
    env.ver = production_latest_version()
    env.next_ver = env.ver + 1

    with cd(env.production_folder):
        # TODO: do backup

        run('mkdir -p v%(next_ver)d' % env)
        with cd('v%(next_ver)d' % env):
            with settings(warn_only=True):
                failed = 0
                while not failed:
                    failed = run('cp -R %(staging_folder)s* .' % env).return_code
                    run('unlink buildout.cfg')
                    failed = run('ln -s buildout.d/production.cfg buildout.cfg').return_code
                    failed = run('cp %(production_django_settings)s intranet/localsettings.py' % env).return_code
                    failed = run('bin/buildout').return_code

                    # everthing went fine.
                    run('../v%(ver)d/bin/supervisorctl shutdown')
                    failed = deploy() is not True

        if failed:
            production_rollback()


def production_latest_version():
    """Version number of latest production dir"""
    versions = sorted(run('find %(production_folder) -name "v*"' % env).split())
    return versions and int(versions[-1].strip('v')) or 0


def production_copy_data_to_staging():
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

    with cd('v%d' % env.prev_ver):
        # TODO: restore backup
        deploy()

    # cleanup
    run('rm -rf v%d' % env.ver)

# TODO: localsettings.py
# TODO: data files
# TODO: set .buildout/default.cfg for env.user with eggs/downloads directory
