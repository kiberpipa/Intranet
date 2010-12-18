# Django settings for intranet project.
import os, re
def next_to_this_file(this_file, additional_path):
    return os.path.join(os.path.dirname(os.path.abspath(this_file)), additional_path)


ADMINS = (
    #('Almir Karic', 'almir@kiberpipa.org'),
    ('Gasper Zejn', 'zejn@kiberpipa.org'),
    ('Domen Kozar', 'domen@dev.si'),
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'sl'

USE_I18N = True 

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

# Make this unique, and don't share it with anybody.
MEDIA_ROOT = next_to_this_file(__file__, '../media')
ADMIN_MEDIA_PREFIX = '/admin-media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'intranet.middleware.Https.Https',
    'intranet.middleware.exception.StandardExceptionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'localeurl.middleware.LocaleURLMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'intranet.middleware.FlatPage.FlatPage',
    'intranet.middleware.NginxCache.NginxMemCacheMiddleWare',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

ROOT_URLCONF = 'intranet.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'intranet.org.context_processors.django_settings',
    'intranet.org.context_processors.media_url',
    'intranet.org.context_processors.admin_media_prefix',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.comments',
    'django.contrib.admin',
    'django.contrib.markup',
    'feedjack', # FIXME
    'localeurl',
    'syncr.twitter',
    'tagging',
    'south',
    'intranet.org',
    'intranet.wiki',
    'intranet.www',
    'pipa.video',
    'pipa.ldap',
    'pipa.ltsp',
    'pipa.mercenaries',
    'pipa.addressbook',
    'pipa.gallery',
)

TEMPLATE_DIRS = (
    next_to_this_file(__file__, 'templates'),
)

FIXTURE_DIRS = (
    next_to_this_file(__file__, 'fixtures'),
)

# 2 weeks
SESSION_COOKIE_AGE = 2209600

AUTH_PROFILE_MODULE = 'addressbook.PipaProfile'
REQUIRE_LOGIN_PATH = '/intranet/accounts/login/'
AUTHENTICATION_BACKENDS = (
    'pipa.ldap.authbackend.LDAPAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LDAP_SERVER='ldap://localhost'
SEND_BROKEN_LINK_EMAILS = True
DEFAULT_FROM_EMAIL = 'intranet@kiberpipa.org'
EMAIL_SUBJECT_PREFIX = '[intranet] '

SERVER_EMAIL = 'intranet@kiberpipa.org'
APPEND_SLASH = True

TWITTER_SYNC = {
    'keywords': ['kiberpipa'],
    'users': ['Kiberpipa', 'FilmSteka', 'cyberpipe', 'MoMoSlo', 'wwwh'],
}

# south
SOUTH_TESTS_MIGRATE = False

# pipa.photo
PHOTOS_FLICKR_IMAGE_URL_S = 'http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s_s.jpg'
PHOTOS_FLICKR_IMAGE_URL = 'http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s.jpg'

from localsettings import *
