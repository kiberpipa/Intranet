
DATABASE_ENGINE = 'mysql'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'intranet2'             # Or path to database file if using sqlite3.
DATABASE_USER = 'intra'             # Not used with sqlite3.
DATABASE_PASSWORD = 'burek182'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/intranet/intranet2/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = 'https://www.kiberpipa.org/~intranet/media/'
ADMIN_MEDIA_PREFIX = 'https://www.kiberpipa.org/~intranet/admin-media/'

BASE_URL = 'http://www.kiberpipa.org'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
#    '/home/intranet/intranet2/templates',
	'/home/redduck666/i/templates/',
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DEBUG = True
#TEMPLATE_DEBUG = DEBUG

#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_BACKEND = 'locmem:///'

CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = "intra"
