from django.conf import settings

def media_url(request):
    return {
        'media_url': settings.MEDIA_URL,
    }

def base_url(request):
    return {
        'base_url': settings.BASE_URL,
    }

def admin_media_prefix(request):
    return {
        'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
    }

def sidebar_slug(request):
    try:
        current_slug = request.META['PATH_INFO']
    except:
        current_slug = ''
    print current_slug
    return {'current_slug': current_slug, }
