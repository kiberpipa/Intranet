from base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': next_to_root('intranet.db'),
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False

# django debug toolbar
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
INTERNAL_IPS = ('127.0.0.1',)

# TODO: use dummy haystack with development
HAYSTACK_SOLR_URL = 'http://localhost:8983/solr/intranet/'
