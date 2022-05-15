from django import forms
from .models import Quotes, Authors, Tags


class QuoteSearchForm(forms.Form):
    author = forms.ModelChoiceField(Authors.objects.order_by('name'), required=False)
    quote = forms.CharField(required=False)


class AuthorSearchForm(forms.Form):
    author = forms.CharField(required=False)


class MyPageQuoteSearchForm(forms.Form):
    quote = forms.CharField(required=False)


class TagsChoiceForm(forms.Form):
    field_name = forms.ModelChoiceField(Tags.objects.order_by('name'), required=True)


class AuthorImageUploadForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ('image',)

