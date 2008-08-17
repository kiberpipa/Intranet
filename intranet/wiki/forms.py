from django import forms
from django.forms import widgets

from models import Article


class ArticleForm(forms.ModelForm):
    comment = forms.CharField(required=False)

    class Meta:
        model = Article

    def clean_name(self):
        import re
        from intranet.wiki.templatetags.wiki import WIKI_WORD

        pattern = re.compile(WIKI_WORD)

        title = self.cleaned_data['title']
        if not pattern.match(title):
            raise forms.ValidationError('Must be a WikiWord.')

        return name
