from django.core.cache import cache
import settings

class NginxMemCacheMiddleWare:
    def process_response(self, request, response):
        cacheIt = False
        theUrl = request.get_full_path()

        for exp in settings.CACHE_INCLUDE_REGEXPS:
            if exp == theUrl:
                cacheIt = True

        # if it's a GET then store it in the cache:
        if request.method != 'GET':
            cacheIt = False

        if cacheIt:
            key = '%s-%s' % (settings.CACHE_KEY_PREFIX,theUrl)
            cache.set(key,response.content)     
        return response
