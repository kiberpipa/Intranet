About
=====

Intranet is a web application based on Django framework for management of information in Kiberpipa NGO. Goal is to refactor current code to smaller modules and port to some existing CMS so that modules could be reused by someone else (eg. hackerspace).


Development setup
=================

Prerequisites::

    sudo apt-get install git python2.7 python2.7-dev python2.7-setuptools libpq-dev libldap2-dev libsasl2-dev

Get Kiberpipa intranet::

    git clone git://github.com/kiberpipa/Intranet.git kiberpipa-intranet
    cd kiberpipa-intranet

Install and run buildout::

    ln -s buildout.d/development.cfg buildout.cfg
    python2.7 bootstrap.py
    bin/buildout

(bootstrap.py is braindead and might want write access to /usr/local/lib/python2.7/dist-packages. The simplest workaround is to temporarily change permissions of that directory to be writeable by your account. You can later delete files bootstrap.py puts there and restore permissions without any obvious problems.)

Copy over default settings::

    cp intranet/localsettings.py.example intranet/localsettings.py

Create the (default is Sqlite3) database::

    bin/django syncdb --all

Django will ask you to create user with administration privileges, follow instructions and remember username/password. Continue with migrations::

    bin/django migrate --fake

Start the development server. Wohoo!::

    bin/django runserver

Load testing data::

    bin/django loaddata initial_db


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

Set the HAYSTACK_SOLR_URL in intranet/localsettings.py::

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
* `cd intranet`
* run `../bin/django makemessages -a` (this will update translation strings into django.po)
* `vim locale/sl/LC_MESSAGES/django.po` and translate new/updated strings
* run `../bin/django compilemessages` (this will generate django.mo file that is used for translations)
* commit django.po and django.mo

Running tests
=============

::

    ./bin/test


Deploying to staging (https://new.kiberpipa.org)
================================================

To first time deploy intranet to hostname:

::

    bin/fab remote_staging_deploy -H HOSTNAME -u REMOTE_USER

For staging to rebuild, you just need to update deploy branch and push::

    git checkout deploy
    git merge master
    git push


Deploying from staging to production
====================================

::

    bin/fab remote_production_deploy -H HOSTNAME -u REMOTE_USER
