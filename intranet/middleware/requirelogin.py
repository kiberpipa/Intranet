#Source:
#http://superjared.com/trac/browser/django/middleware/requirelogin.py

from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

class RequireLoginMiddleware(object):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication.
    
    If an anonymous user requests a page, he/she is redirected to the login
    page set by REQUIRE_LOGIN_PATH or /accounts/login/ by default.
    """
    def __init__(self):
	    self.require_login_path = getattr(settings, 'REQUIRE_LOGIN_PATH', '/accounts/login/')
	
    def process_request(self, request):
        excludes = ['/zavod/', '/intranet/feeds/', '/intranet/stats/text_log', '/smedia/', '/amedia/', '/']
        for i in excludes:
          if i in request.path:
            return None
          
        if request.path != self.require_login_path and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
                
