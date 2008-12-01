from django.conf import settings
class Https(object):
    def process_request(self, request):
        if request.META['wsgi.url_scheme'] == 'https':
            settings.ADMIN_MEDIA_PREFIX = 'https://www.kiberpipa.org/admin-media/'
            settings.MEDIA_URL = 'https://www.kiberpipa.org/media/'
        return None

