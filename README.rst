About
=====

Intranet is a web application based on Django framework for management of information in Kiberpipa hackerspace.
Goal is to refactor current code to smaller modules and port to some existing CMS so that modules could be
reused by someone else (eg. hackerspace).


Development setup
=================

Get development enironment::

    $ git clone https://github.com/kiberpipa/Intranet.git kiberpipa-intranet
    $ cd kiberpipa-intranet
    $ make
    
Copy over default settings::

    $ cp intranet/settings/local.py.example intranet/settings/local.py

Create (default is Sqlite3) database::

    $ django-admin.py syncdb --all

Django will ask you to create user with administration privileges, follow instructions and remember username/password.
Continue by faking migrations::

    $ django-admin.py migrate --fake

Load testing data::

    $ django-admin.py loaddata initial_db
    
Start the development server. Wohoo!::

    $ django-admin.py runserver


Running tests
=============

::

    make test


Solr setup
==========

If you want search to work you also need to setup a development instance of Solr.

Get the latest Apache Solr binary distribution::

    wget http://apache.mirrors.hoobly.com/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
    tar -xzf apache-solr-3.5.0.tgz

Update the schema::

    bin/django build_solr_schema > apache-solr-3.5.0/example/solr/conf/schema.xml

Add MoreLikeThisHandler to apache-solr-3.5.0/example/solr/conf/solrconfig.xml. Append the following lines inside the <config> tag::

    <requestHandler name="/mlt" class="solr.MoreLikeThisHandler">
      <lst name="defaults">
        <int name="mlt.mindf">1</int>
      </lst>
    </requestHandler>

Set the HAYSTACK_SOLR_URL in intranet/settings/local.py::

    HAYSTACK_SOLR_URL = 'http://localhost:8983/solr/'

Start the server. Yay!::

    cd apache-solr-3.5.0/example
    java -jar start.jar


Coding standards
================

* all code MUST be written in English
* `PEP8 coding style <http://www.python.org/dev/peps/pep-0008/>`_ should be followed except 80 char line limit


Managing with translations
==========================

* First you have to make some changes to translated strings (either in templates or code itself)
* run `bin/django makemessages -a` (this will update translation strings into django.po)
* `vim locale/sl/LC_MESSAGES/django.po` and translate new/updated strings
* run `bin/django compilemessages` (this will generate django.mo file that is used for translations)
* commit django.po and django.mo




Restoring database
================== 

::

    createuser -p 5433 -P i3
    createdb -p 5433 i3
    psql -p 5433
    GRANT ALL PRIVILEGES ON DATABASE i3 TO i3;
    pg_restore --list db.sql | grep -v LANGUAGE | grep -v FUNCTION | grep -v AGGREGATE > db.list
    pg_restore -Fc --no-acl -e --no-owner -p 5433 -U i3 -d i3 -L db.list db.sql
    mkdir media
    cd media
    tar xf ../mediafiles.tar.gz
