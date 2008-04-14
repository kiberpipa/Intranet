from django.db import models
from django.db.models.loading import get_app

class Tag(models.Model):
  value = models.CharField(max_length=50)
  norm_value = models.CharField(max_length=50, editable=False)
  
  class Meta:
    ordering=('norm_value','value')
  
  def __str__(self):
    return self.value
    
  def save(self):
    tags = get_app('tags')
    from tags.utils import normalize_title
    self.norm_value = normalize_title(self.value)
    super(Tag, self).save()
