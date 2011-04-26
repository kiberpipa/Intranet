from urlparse import urlsplit
from django import http
from django.utils.translation import check_for_language
from localeurl import utils

def change_locale(request):
    """
    Redirect to a given url while changing the locale in the path
    The url and the locale code need to be specified in the
    request parameters.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    next = urlsplit(next).path
    _, path = utils.strip_path(next)
    if request.method == 'POST':
        locale = request.POST.get('locale', None)
        if locale and check_for_language(locale):
            path = utils.locale_path(path, locale)

    response = http.HttpResponseRedirect(path)
    return response
