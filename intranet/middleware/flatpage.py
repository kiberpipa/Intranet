#hack to make flat pages play nicely with localeurl middleware
# basically it does this:
# - reattach the language code prefix (only if it has been stripped)
# - calculate the flat page (if any)
# - restore path_info
# - return whatever the django stock middleware returned to us

from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware


class FlatPageLocaleURLFallbackMiddleware(FlatpageFallbackMiddleware):
    def process_response(self, request, response):
        orig = request.path_info
        if hasattr(request, 'LANGUAGE_CODE'):
            request.org_path_info = request.path_info
            request.path_info = '/' + request.LANGUAGE_CODE + request.path_info
        ret = super(FlatPageLocaleURLFallbackMiddleware, self).process_response(request, response)
        request.path_info = orig
        return ret
