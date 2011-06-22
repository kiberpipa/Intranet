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

    ./manage.py syncdb --all
    ./manage.py migrate --fake

Start the development server. Wohoo!::

    ./manage.py runserver


Running tests
=============

::

    ./manage.py test org www


Deploying to staging (https://new.kiberpipa.org)
================================================

::

    git co deploy
    git merge master
    ssh <dogbert>
    su - intranet
    ~/bin/testdeploy

To refresh db from production to staging, do::

    su - djangotest
    ~/bin/sqlreload-intranet


Deploying from staging to production
====================================

::

    ssh <dogbert>
    su - intranet
    ~/bin/deploy intranet v<current>+1
    ~/bin/runintranet v<current>+1
