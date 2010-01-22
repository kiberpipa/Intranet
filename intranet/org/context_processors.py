from django.conf import settings

def media_url(request):
    return {
        'media_url': settings.MEDIA_URL,
    }

def admin_media_prefix(request):
    return {
        'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
    }
