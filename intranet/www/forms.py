from django import forms

from photologue.models import GalleryUpload


class FileForm(forms.ModelForm):
    class Meta:
        model = GalleryUpload
        fields = ('zip_file',)
