#FlatPage wrapper to reattach language prefix to flat pages
from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware
from os.path import join

class FlatPage(FlatpageFallbackMiddleware):
    def process_response(self, request, response):
        request.path_info = join('/' + request.LANGUAGE_CODE, request.path_info[1:])
        return super(FlatPage, self).process_response(request, response)
