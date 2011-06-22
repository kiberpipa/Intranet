#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='intranet',
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
        'Pillow',  # proper distributed PIL
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
        'Django>=1.3,<1.4',
        'django-localeurl',
        'django-tagging',
        'South',
        'flickrapi',
        'django-syncr',
        'django-honeypot',
        'python-dateutil',
        'django-reversion',
        # commands
        'twitter',
    ],
    tests_require=[
        'nose',
    ],
)
