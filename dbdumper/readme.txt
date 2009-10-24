
Intranet database dumper/loader
===============================

Using PostgreSQL
----------------

Step 1: Clear the database
(Assuming database named i)

  pgsql> DROP DATABASE i; CREATE DATABASE i WITH OWNER i;

Step 2: Do a syncdb

  echo no | ./manage.py syncdb

Step 3: Load the data

  cd rd666/dbdumper && ./load.sh


