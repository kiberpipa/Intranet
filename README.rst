Development setup
=================

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
    bin/django migrate --fake

Start the development server. Wohoo!::

    bin/django runserver


Running tests
=============

::

    ./bin test


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
