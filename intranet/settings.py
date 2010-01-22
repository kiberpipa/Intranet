# Django settings for intranet project.
import os, re
def next_to_this_file(this_file, additional_path):
    return os.path.join(os.path.dirname(os.path.abspath(this_file)), additional_path)


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    #('Almir Karic', 'almir@kiberpipa.org'),
    ('Gasper Zejn', 'zejn@kiberpipa.org'),
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Vienna'

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
    re.compile('^comments/post/$'),
    re.compile('^news/comments/post/$'),
    re.compile('^comments/'),
    re.compile('event_photos/'),
    re.compile('^favicon.ico'),
    re.compile('^/services/'),
)

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x&@ve8lp+4g3%^hgigvuv3svcig^3jbz@&w=_e4h#vaw2#odmg'
MEDIA_ROOT = next_to_this_file(__file__, '../media')
ADMIN_MEDIA_PREFIX = '/admin-media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'intranet.middleware.Https.Https',
    'intranet.middleware.exception.StandardExceptionMiddleware',
    #'intranet.middleware.psyco_middleware.PsycoMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'localeurl.middleware.LocaleURLMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'intranet.middleware.requirelogin.RequireLoginMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'intranet.middleware.FlatPage.FlatPage',
    #'intranet.stats.StatsMiddleware',
    'middleware.NginxCache.NginxMemCacheMiddleWare',
)

ROOT_URLCONF = 'intranet.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'intranet.org.context_processors.media_url',
    'intranet.org.context_processors.admin_media_prefix',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'intranet.org',
    'django.contrib.comments',
    'intranet.wiki',
    'django.contrib.admin',
    'django.contrib.markup',
    'intranet.www',
    'photologue',
    'feedjack', # FIXME
    'localeurl',
    'pipa.video',
    'pipa.ldap',
    'pipa.ltsp',
    'pipa.mercenaries',
    'pipa.addressbook',
    'syncr.twitter',
    'tagging',
)

TEMPLATE_DIRS = (
    next_to_this_file(__file__, 'templates'),
)

FIXTURE_DIRS = (
    next_to_this_file(__file__, 'fixtures'),
)

AUTH_PROFILE_MODULE = 'addressbook.PipaProfile'
REQUIRE_LOGIN_PATH = '/intranet/accounts/login/'
AUTHENTICATION_BACKENDS = (
    'pipa.ldap.authbackend.LDAPAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
PHOTOLOGUE_DIR = 'photo/'

GALLERY_SAMPLE_SIZE = 1
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

from localsettings import *
