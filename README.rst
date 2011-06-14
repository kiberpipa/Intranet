Development setup
=================

Get intranet::

    git clone git://github.com/kiberpipa/Intranet.git kiberpipa-intranet
    cd kiberpipa-intranet

Create Python virtual environment and activate it::

    virtualenv --no-site-packages --python=/usr/bin/python2.6 .
    source bin/activate

Install intranet::

    python setup.py develop

(optional) install database driver - default is sqlite3::

    # for postgres
    easy_install psycopg2
    # for mysql
    easy_install mysql-python

Copy over default settings::

    cd intranet
    cp localsettings.py.example localsettings.py

Create the (default is Sqlite3) database::

    ./manage.py syncdb --all

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
