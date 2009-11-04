
Development setup
=================

Get required packages

$ sudo apt-get install python-reportlab

Get intranet

$ svn co https://www.kiberpipa.org/svn/intranet/rd666

change dir to checked out project..

$ cd rd666

Copy over default settings..

$ cp localsettings.py.example localsettings.py

Create the (default is Sqlite3) database..

$ ./manage.py syncdb

Start the development server. Wahoo!

$ ./manage.py runserver


