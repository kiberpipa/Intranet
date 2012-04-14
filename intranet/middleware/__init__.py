from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware


class IgnoreBrowserLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class FlatPageLocaleURLFallbackMiddleware(FlatpageFallbackMiddleware):
    """Trick to make flat pages play nicely with i18n_patterns. Try:

     - attach language code to url and find flatpage
     - find flatpage without language code

    """

    def process_response(self, request, response):
        # attach language code to url and find flatpage
        orig = request.path_info
        if hasattr(request, 'LANGUAGE_CODE'):
            request.path_info = '/' + request.LANGUAGE_CODE + request.path_info
        ret = super(FlatPageLocaleURLFallbackMiddleware, self).process_response(request, response)
        request.path_info = orig

        # find flatpage without language code
        if not ret:
            ret = super(FlatPageLocaleURLFallbackMiddleware, self).process_response(request, response)

        return ret
