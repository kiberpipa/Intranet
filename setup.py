#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


setup(name='kiberpipa-intranet',
    version='0.1',
    description="",
    long_description="""""",
    keywords='',
    author='',
    author_email='',
    url='http://www.kiberpipa.org',
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    packages=find_packages(),
    classifiers=[
    ],
    install_requires=[
        'BeautifulSoup',
        'python-ldap',
        'Pillow', # proper distributed PIL
        'feedjack',
        'reportlab',
        'PyExcelerator',
        'egenix-mx-base',
        'pytz',
        'pygments',
        'simplejson',
        # wiki
        'markdown2',
        # django stuff
        'Django==1.3',
        'django-localeurl',
        'django-tagging==0.3.1',
        'South',
        'flickrapi',
        'django-syncr',
        'django-honeypot',
        'python-dateutil',
        'django-reversion',
    ],
    tests_require=[
        'nose',
    ],
    extras_require={
    },
    entry_points={
    },
)
