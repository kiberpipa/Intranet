from haystack.indexes import *
from haystack import site

from intranet.org.models import Event


class EventIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    title = CharField(model_attr="title")
    start_date = DateTimeField(model_attr="start_date")
    end_date = DateTimeField(model_attr="end_date")

    # booleans
    require_video = BooleanField(model_attr="require_video")
    require_photo = BooleanField(model_attr="require_photo")
    require_technician = BooleanField(model_attr="require_technician")
    is_public = BooleanField(model_attr="public")


site.register(Event, EventIndex)

# WARNING: if you change schema of any search index, you must update solr schema manually!
# TODO: http://docs.haystacksearch.org/dev/installing_search_engines.html?highlight=more%20like#solr
# TODO: mavrik schema config, binary, so
# edit solrconfig with more like this handler
# insert text analyzer chain
# wget http://trac.greenstone.org/browser/gs3-extensions/solr/trunk/src/conf/mapping-FoldToASCII.txt
