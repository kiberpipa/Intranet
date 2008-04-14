from django.db.models.fields import ImageField
from utils import make_thumbnail, _remove_thumbnails, remove_model_thumbnails, rename_by_field
from django.dispatch import dispatcher
from django.db.models import signals

def _delete(instance=None):
    if instance:
        print '[thumbnail] DELETE', instance
        remove_model_thumbnails(instance)
#

class ImageWithThumbnailField(ImageField):
    """ ImageField with thumbnail support
    
        auto_rename: if it is set perform auto rename to
        <class name>-<field name>-<object pk>.<ext>
        on pre_save.
    """

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, auto_rename=True, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        super(ImageWithThumbnailField, self).__init__(verbose_name, name, width_field, height_field, **kwargs)
        self.auto_rename = auto_rename
    #
    
    def _save(self, instance=None):
        if not self.auto_rename: return
        if instance == None: return
        image = getattr(instance, self.attname)
        # XXX this needs testing, maybe it can generate too long image names (max is 100)
        image = rename_by_field(image, '%s-%s-%s' \
                                     % (instance.__class__.__name__,
                                         self.name,
                                         instance._get_pk_val()
                                        )
                                   )
        setattr(instance, self.attname, image)
    #
    
    def contribute_to_class(self, cls, name):
        super(ImageWithThumbnailField, self).contribute_to_class(cls, name)
        dispatcher.connect(_delete, signals.post_delete, sender=cls)
        dispatcher.connect(self._save, signals.pre_save, sender=cls)
    #

    def get_internal_type(self):
        return 'ImageField'
    #
#
