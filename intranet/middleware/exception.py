#from http://www.djangosnippets.org/snippets/638/

from django.conf import settings
from django import http
from django.core.mail import send_mail


import sys

# Temporary, from http://code.djangoproject.com/attachment/ticket/6094/6094.2008-02-01.diff
from django.core.urlresolvers import RegexURLResolver
def resolver(request):
    """
    Returns a RegexURLResolver for the request's urlconf.

    If the request does not have a urlconf object, then the default of
    settings.ROOT_URLCONF is used.
    """
    from django.conf import settings
    urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
    return RegexURLResolver(r'^/', urlconf)


class StandardExceptionMiddleware(object):
    def process_exception(self, request, exception):
        self.log_exception(request, exception, sys.exc_info())
        # Get the exception info now, in case another exception is thrown later.
        if isinstance(exception, http.Http404):
            return self.handle_404(request, exception)
        else:
            return self.handle_500(request, exception)

        # in re https://www.kiberpipa.org/intranet/bugs/157/
        # rethrow exception to preserve call stack
        raise


    def handle_404(self, request, exception):
        if settings.DEBUG:
            from django.views import debug
            return debug.technical_404_response(request, exception)
        else:
            callback, param_dict = resolver(request).resolve404()
            return callback(request, **param_dict)


    def handle_500(self, request, exception):
        exc_info = sys.exc_info()
        if settings.DEBUG:
            return self.debug_500_response(request, exception, exc_info)
        else:
            return self.production_500_response(request, exception, exc_info)


    def debug_500_response(self, request, exception, exc_info):
        from django.views import debug
        return debug.technical_500_response(request, *exc_info)


    def production_500_response(self, request, exception, exc_info):
        '''Return an HttpResponse that displays a friendly error message.'''
        callback, param_dict = resolver(request).resolve500()
        return callback(request, **param_dict)


    def exception_email(self, request, exc_info):
        subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
        try:
            request_repr = repr(request)
        except:
            request_repr = "Request repr() unavailable"
        message = "%s\n\n%s" % (_get_traceback(exc_info), request_repr)
        return subject, message


    def log_exception(self, request, exception, exc_info):
        subject, message = self.exception_email(request, exc_info)
        send_mail(subject, message, 'intranet@kiberpipa.org', [a[1] for a in settings.ADMINS], fail_silently=True)


def _get_traceback(self, exc_info=None):
    """Helper function to return the traceback as a string"""
    import traceback
    return '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
