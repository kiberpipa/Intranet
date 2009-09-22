#hack to make flat pages play nicelly with localeurl middleware
# basically it does this:
# - reattach the language code prefix (only if it has been stripped)
# - calculate the flat page (if any)
# - restore path_info
# - return whatever the django stock middleware returned to us
from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware
from os.path import join

class FlatPage(FlatpageFallbackMiddleware):
    def process_response(self, request, response):
        orig = request.path_info
        if not hasattr(self, 'LANGUAGE_CODE'):
            request.is_flatpage = True
            request.org_path_info = request.path_info
            request.path_info = join('/' + request.LANGUAGE_CODE, request.path_info[1:])
        ret = super(FlatPage, self).process_response(request, response)
        request.path_info = orig
        return ret
