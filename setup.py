#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='intranet',
    version='0.1',
    description="",
    long_description="""""",
    keywords='',
    author='',
    author_email='info@kiberpipa.org',
    url='http://www.kiberpipa.org',
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    packages=find_packages(),
    classifiers=[
    ],
    install_requires=[
        # deprecated
        'BeautifulSoup',
        'simplejson',  # TODO: use json
        # other
        'reportlab',
        'PyExcelerator',
        'html2text',
        'pytz',
        'pygments',
        'Fabric',
        # intranet.org
        'python-ldap',
        'django-tinymce',
        # intranet.www
        'python-memcached',
        'flickrapi',
        'requests',
        'python-dateutil',
        'python-twitter',
        'django-mailman',
        'django-spaminspector',
        'akismet',
        'icalendar',
        'pytz',
        # django stuff
        'Django>=1.4',
        'Feedjack',
        'django-tagging',
        'Pillow',  # properly distributed PIL
        'South',
        'django-honeypot',
        'django-grappelli',
        'django-gravatar2',
        'django-chosen',
        # development
        'django-extensions',
        'django-coverage',
        'coverage',
        # solr
        'django-haystack',
        'pysolr',
        # database
        'psycopg2',
        'egenix-mx-base',
        # admin
        'raven',
        'django-reversion',
        'facebook-sdk',
    ],
    tests_require=[
        'nose',
    ],
    extras_require={
        'develop': ["bpython", 'django-debug-toolbar', 'Werkzeug'],
        'deploy': ["gunicorn"],
    },
)
