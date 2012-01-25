import os
import urllib2
from zipfile import ZipFile
from cStringIO import StringIO

import requests
from django.template import Template, Context
from django.http import HttpResponse
from django.conf import settings


def _sablona_file(fn):
    return os.path.join(os.path.dirname(__file__), 'sablona', fn)


def prepare_video_zip(slug, title, date, person):
    context = Context({
        'date': title,
        'title': date,
        'predavatelji': person,
    })

    folder_title = slug

    t = Template(open(_sablona_file('default.xml')).read())
    default_xml = t.render(context).encode('utf-8')

    zipfile_file = StringIO()
    zipfile = ZipFile(zipfile_file, "w")
    zipfile.writestr("%s/default.xml" % folder_title, default_xml)

    for fn in ['big_pal_1_2-page3.png', 'big_pal_1_2-page4.png', 'maska_small.png', 'naslovnica_small.png', 'readme']:
        zipfile.write(_sablona_file(fn), '%s/%s' % (folder_title, fn))

    zipfile.close()

    response = HttpResponse(zipfile_file.getvalue(), mimetype="application/zip")
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % folder_title
    return response


def is_streaming():
    """Check if video live stream is running."""
    r = requests.head(settings.LIVE_STREAM_URL)
    return 200 < r.status_code < 300
