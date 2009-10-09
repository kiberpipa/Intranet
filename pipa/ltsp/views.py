import simplejson

from django.http import HttpResponseRedirect, HttpResponse
from pipa.ltsp.models import Usage


def internet_usage_report(request):
    """
    LTSP reporting internet usage.
    
    To use it, you need to do a POST request with parameters
    data and sign, data is json encoded dict with datetime and count.
    Example:
    
     {'time': [2009, 3, 2, 22, 37, 23, 0], 'count': 10}
    
    sign(ature) is a MD5 hash of serialized JSON with appended shared secret.
    """
    if not request.method == 'POST':
        raise Http404

    data = request.POST.get('data', None)
    sign = request.POST.get('sign', None)

    if not data or not sign:
        return HttpResponse("Sorry.")

    try:
        json = simplejson.loads(data)
    except ValueError:
        return HttpResponse("Sorry. Not a JSON.")
    t, all = json.get('time', ''), json.get('count', 0)

    if sign == md5.new(data + settings.LTSP_USAGE_SECRET).hexdigest():
        cnt = Usage(time=datetime.datetime(*t), count=all)
        cnt.save()
        print cnt.count, cnt.time
    else:
        return HttpResponse("Sorry, but no thanks.")
    return HttpResponse("Thanks.")
