Development setup
=================

Get intranet::

	svn co https://www.kiberpipa.org/svn/intranet/rd666 kiberpipa-intranet
    cd kiberpipa-intranet

Create Python virtual environment and activate it:

    virtualenv --no-site-packages --python=/usr/bin/python2.6 .
    source bin/activate

Install intranet::

    python setup.py develop

(optional) install database driver::

    # for postgres
    easy_install psycopg2
    # for mysql
    easy_install mysql-python

Copy over default settings::

    cd intranet
	cp localsettings.py.example localsettings.py

Create the (default is Sqlite3) database::

	./manage.py syncdb

Start the development server. Wahoo!::

	./manage.py runserver


RUNNING TESTS
=============

    ./manage.py test
