Development setup
=================

Prerequisites::

    sudo apt-get install git python2.7 libpq-dev libldap2-dev libsasl2-dev

Get Kiberpipa intranet::

    git clone git://github.com/kiberpipa/Intranet.git kiberpipa-intranet
    cd kiberpipa-intranet

Install and run buildout::

    ln -s buildout.d/development.cfg buildout.cfg
    python2.7 bootstrap.py
    bin/buildout

Copy over default settings::

    cp intranet/localsettings.py.example intranet/localsettings.py

Create the (default is Sqlite3) database::

    bin/django syncdb --all

Django will ask you to create user with administration privileges, follow instructions and remember username/password. Continue with migrations::

    bin/django migrate --fake

Start the development server. Wohoo!::

    bin/django runserver


Coding standards
================

* all code MUST be written in English
* `PEP8 coding style <http://www.python.org/dev/peps/pep-0008/>`_ should be followed except 80 char line limit


Managing with translations
==========================

* First you have to make some changes to translated strings (either in templates or code itself)
* `cd intranet`
* run `../bin/django makemessages -a` (this will update translation strings into django.po)
* `vim locale/sl/LC_MESSAGES/django.po` and translate new/updated strings
* run `../bin/django compilemessages -a` (this will generate django.mo file that is used for translations)
* commit django.po and django.mo

Running tests
=============

::

    ./bin/test


Deploying to staging (https://new.kiberpipa.org)
================================================

To first time deploy intranet to hostname:

::

    bin/fab staging_deploy -H hostname

For staging to rebuild, you just need to update deploy branch and push::

    git checkout deploy
    git merge master
    git push


Deploying from staging to production
====================================

::

    bin/fab production_deploy -H hostname
