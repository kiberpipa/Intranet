from django.conf import settings
from django import http
from django.core.urlresolvers import resolve

class SmartAppendSlashMiddleware(object):
    """
    "SmartAppendSlash" middleware for taking care of URL rewriting.

    This middleware appends a missing slash, if:
    * the SMART_APPEND_SLASH setting is True
    * the URL without the slash does not exist
    * the URL with an appended slash does exist.
    Otherwise it won't touch the URL.
    """

    def process_request(self, request):
        """
        Rewrite the URL based on settings.SMART_APPEND_SLASH
        """

        # Check for a redirect based on settings.SMART_APPEND_SLASH
        host = http.get_host(request)
        old_url = [host, request.path]
        new_url = old_url[:]
        # Append a slash if SMART_APPEND_SLASH is set and the resulting URL
        # resolves.
        if settings.SMART_APPEND_SLASH and (not old_url[1].endswith('/')) and not _resolves(old_url[1]) and _resolves(old_url[1] + '/'):
            new_url[1] = new_url[1] + '/'
            if settings.DEBUG and request.method == 'POST':
                raise RuntimeError, "You called this URL via POST, but the URL doesn't end in a slash and you have SMART_APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to %s%s (note the trailing slash), or set SMART_APPEND_SLASH=False in your Django settings." % (new_url[0], new_url[1])
        if new_url != old_url:
            # Redirect
            if new_url[0]:
                newurl = "%s://%s%s" % (request.is_secure() and 'https' or 'http', new_url[0], new_url[1])
            else:
                newurl = new_url[1]
            if request.GET:
                newurl += '?' + request.GET.urlencode()
            return http.HttpResponsePermanentRedirect(newurl)

        return None

def _resolves(url):
    try:
        resolve(url)
        return True
    except http.Http404:
        return False

