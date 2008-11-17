from django.core.cache import cache
from django.http import HttpResponseNotFound
import re
import settings

class NginxMemCacheMiddleWare:
    def process_response(self, request, response):
        if isinstance(response, HttpResponseNotFound):
            return response

        try:
            settings.CACHE_IGNORE_REGEXPS
        except AttributeError:
            return response

        cacheIt = True
        theUrl = request.get_full_path()

        # if it's a GET then store it in the cache:
        if request.method != 'GET':
            cacheIt = False

        # loop on our CACHE_INGORE_REGEXPS and ignore
        # certain urls.
        for exp in settings.CACHE_IGNORE_REGEXPS:
            if re.match(exp,theUrl):
                cacheIt = False

        if cacheIt:
            key = '%s-%s' % (settings.CACHE_KEY_PREFIX,theUrl)
            cache.set(key,response.content)     


        return response
