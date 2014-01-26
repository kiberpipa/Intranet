from haystack import indexes

from intranet.org.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    title = indexes.CharField(model_attr="title")
    start_date = indexes.DateTimeField(model_attr="start_date")
    end_date = indexes.DateTimeField(model_attr="end_date")

    # booleans
    require_video = indexes.BooleanField(model_attr="require_video")
    require_photo = indexes.BooleanField(model_attr="require_photo")
    require_technician = indexes.BooleanField(model_attr="require_technician")
    is_public = indexes.BooleanField(model_attr="public")

    def get_model(self):
        return Event


# WARNING: if you change schema of any search index, you must update solr schema manually!
# TODO: http://docs.haystacksearch.org/dev/installing_search_engines.html?highlight=more%20like#solr
# TODO: mavrik schema config, binary, so
# edit solrconfig with more like this handler
# insert text analyzer chain
# wget http://trac.greenstone.org/browser/gs3-extensions/solr/trunk/src/conf/mapping-FoldToASCII.txt
