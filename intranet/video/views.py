from intranet.video.models import Video, VideoCategory
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django import newforms as forms

# Create your views here.

def cat_index(request, category):
    cat = VideoCategory.objects.get(slug__exact=category)
    cats = cat.video_set.all()
    return render_to_response('video/video_archive.html',
                              { 'latest': cats,
                              },
                              context_instance=RequestContext(request))

def upload(request):
    f_choices = [('1','Bla'),('2','Buga'),('3','Bingo')]
    class Step1(forms.Form):
      file_list = forms.ChoiceField(choices=f_choices,
                                    widget=forms.RadioSelect)
    
    if request.POST:
      data = request.POST
    else:
      data = {'file_list': '1', }
    
    myform = Step1(data)
    
    return render_to_response('video/upload.html',
                              { 'myform': myform, },
                              context_instance=RequestContext(request))