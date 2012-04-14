from base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = True

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
