import os
import re


def next_to_this_file(this_file, additional_path):
    return os.path.join(os.path.dirname(os.path.abspath(this_file)), additional_path)


ADMINS = (
    ('Gasper Zejn', 'zejn@kiberpipa.org'),
    ('Domen Kozar', 'domen@dev.si'),
)
MANAGERS = (
    ('Gasper Zejn', 'zejn@kiberpipa.org'),
)

TIME_ZONE = 'Europe/Ljubljana'
LANGUAGE_CODE = 'sl'

USE_I18N = True
USE_L10N = True

LANGUAGES = (
  ('sl', 'Slovenscina'),
  ('en', 'English'),
)

# localeurl
LOCALE_INDEPENDENT_PATHS = (
    re.compile('^/intranet/'),
    re.compile('^(modules|index)\.php'),
    re.compile('^rss/?$'),
    re.compile('ajax/'),
    re.compile('[as]media/'),
    re.compile('/i18n/setlang/'),
    re.compile('/jsi18n/'),
    re.compile('^news/comments/post/$'),
    re.compile('^comments/'),
    re.compile('^comments/post/$'),
    re.compile('event_photos/'),
    re.compile('^favicon.ico'),
    re.compile('^/services/'),
)

SITE_ID = 1

MEDIA_URL = '/smedia/'
MEDIA_ROOT = next_to_this_file(__file__, '../media')
STATIC_URL = '/static/'
STATIC_ROOT = next_to_this_file(__file__, '../static')
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'sentry.client.middleware.Sentry404CatchMiddleware',  # must be first, to catch all good responses
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'localeurl.middleware.LocaleURLMiddleware',
    'honeypot.middleware.HoneypotMiddleware',  # as soon as possible
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'intranet.middleware.flatpage.FlatPageLocaleURLFallbackMiddleware',
)

ROOT_URLCONF = 'intranet.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'intranet.org.context_processors.django_settings',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.comments',
    'grappelli',  # must be before admin
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.staticfiles',
    'reversion',
    'feedjack',  # FIXME
    'localeurl',
    'syncr.twitter',
    'tagging',
    'south',
    'intranet.org',
    'intranet.www',
    'pipa.video',
    'pipa.ldap',
    'pipa.ltsp',
    'pipa.mercenaries',
    'pipa.addressbook',
    'pipa.gallery',
    'honeypot',
    'django_extensions',
    'sentry',
    'sentry.client',
    'django_mailman',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'sentry.client.handlers.SentryHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '()': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'intranet': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'pipa': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


TEMPLATE_DIRS = (
    next_to_this_file(__file__, 'templates'),
)

FIXTURE_DIRS = (
    next_to_this_file(__file__, 'fixtures'),
)

# 2 weeks
SESSION_COOKIE_AGE = 2209600

AUTH_PROFILE_MODULE = 'addressbook.PipaProfile'
LOGIN_REDIRECT_URL = '/intranet/accounts/profile/'
LOGIN_URL = '/intranet/accounts/login/'
LOGOUT_URL = '/intranet/accounts/logout/'
AUTHENTICATION_BACKENDS = (
    'pipa.ldap.authbackend.LDAPAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LDAP_SERVER = 'ldap://localhost'
SEND_BROKEN_LINK_EMAILS = True
DEFAULT_FROM_EMAIL = 'intranet@kiberpipa.org'
EMAIL_SUBJECT_PREFIX = '[intranet] '

SERVER_EMAIL = 'intranet@kiberpipa.org'
APPEND_SLASH = True

TWITTER_SYNC = {
    'keywords': ['kiberpipa'],
    'users': ['Kiberpipa', 'FilmSteka', 'cyberpipe', 'MoMoSlo', 'wwwh'],
}

# haystack
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SITECONF = 'intranet.haystacksearch'
HAYSTACK_SOLR_URL = 'http://localhost:8983/solr/intranet/'

# south
SOUTH_TESTS_MIGRATE = False

# pipa.photo
PHOTOS_FLICKR_IMAGE_URL_S = 'http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s_s.jpg'
PHOTOS_FLICKR_IMAGE_URL = 'http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s.jpg'

# pipa.video
LIVE_STREAM_URL = 'http://kiberpipa.org:8000/kiberpipa.ogg'
PUBLIC_LIVE_STREAM_URL = 'http://video.kiberpipa.org/live.html'

# honeypot
HONEYPOT_FIELD_NAME = "enter_your_email"

from localsettings import *
