

from django.utils.translation import ugettext_lazy as _


def generate_menu(request):
    language = request.LANGUAGE_CODE
    return {'menu': [
        {'url': '/%s/about/' % language, 'name': _('about')},
        {'url': '/%s/calendar/' % language, 'name': _('calendar')},
        {'url': 'http://www.flickr.com/photos/kiberpipa/collections/',
         'name': _('gallery')},
#        {'url': 'http://video.kiberpipa.org/', 'name': _('video')},
        {'url': '/%s/alumni/' % language, 'name': _('community')},
        {'url': '/%s/support/' % language, 'name': _('support')},
    ]}
