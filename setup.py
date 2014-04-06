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
        # other
        'html2text',
        'pytz',
        'pygments',
        # intranet.org
        'python-ldap',
        'passlib',
        'django-tinymce',
        # intranet.www
        'flickrapi',
        'requests',
        'python-dateutil',
        'python-twitter',
        'django-mailman',
        'django-akismet-comments',
        'icalendar',
        'django-activelink',
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
        # solr
        'django-haystack',
        'pysolr',
        # database
        'psycopg2',
        # admin
        'raven',
        'django-reversion',
    ],
    tests_require=[
        'nose',
    ],
    extras_require={
        'develop': ["bpython", 'django-debug-toolbar', 'Werkzeug'],
        'deploy': ["gunicorn"],
    },
)
