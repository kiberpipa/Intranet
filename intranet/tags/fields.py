# -*- coding:utf-8 -*-
from django.db import models
from django import forms
from django.template import loader, Context
from django.db.models.loading import get_app, get_model
from django.conf import settings

def get_id(model, value):
  if not value:
    return ''
  tags = get_app('tags')
  from tags.utils import normalize_title
  obj_list = model.objects.filter(norm_value__exact=normalize_title(value))
  if len(obj_list):
    return int(obj_list[0].id)
  else:
    obj = model(value=value)
    print "sejvam ", obj
    obj.save()
    return int(obj.id)
    
class TagsFormField(forms.FormField):
  requires_data_list = True
  def __init__(self, field_name, is_required=False, validator_list=[]):
    self.field_name = field_name
    self.is_required = is_required
    self.validator_list = validator_list
    
  def get_validation_errors(self, new_data):
    if new_data.has_key(self.field_name):
      new_data.setlist(self.field_name, [v for v in new_data.getlist(self.field_name) if v != ''])
    return forms.FormField.get_validation_errors(self, new_data)
  
  def convert_post_data(self, new_data):
    if new_data.has_key(self.field_name):
      new_data.setlist(self.field_name, [v for v in new_data.getlist(self.field_name) if v != ''])
    forms.FormField.convert_post_data(self, new_data)
    
  def render(self, data):
    print "render:data", data
    Tag = get_model('tags', 'Tag')
    if data:
      initial_tags = Tag.objects.filter(id__in=data)
    else:
      initial_tags = []
    template = loader.get_template('tags/tag_widget.html')
    context = Context({
      'tags': Tag.objects.all(),
      'initial_tags': initial_tags,
      'style_url': hasattr(settings, 'STYLE_URL') and settings.STYLE_URL or '/media/css/',
      'js_url': hasattr(settings, 'JS_URL') and settings.JS_URL or '/media/js/',
      'tags_url': hasattr(settings, 'TAGS_URL') and settings.TAGS_URL or '/tags/',
    })
    return template.render(context)
    
  def html2python(data):
    Tag = get_model('tags', 'Tag')
    return get_id(Tag, data)
  html2python = staticmethod(html2python)

class TagsField(models.ManyToManyField):
  def get_manipulator_field_objs(self):
    return [TagsFormField]
    
  def flatten_data(self, follow, obj=None):
    new_data = {}
    if obj:
      new_data[self.name] = [int(instance.id) for instance in getattr(obj, self.name).all()]
    return new_data
