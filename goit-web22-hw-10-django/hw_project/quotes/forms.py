from django.db.models import TextField
from django import forms
from django.forms import ModelForm, CharField, DateField, DateTimeField, TextInput

from .models import Author, Quote


class AuthorForm(forms.ModelForm):
    born_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea, label='Quote')
    author = forms.ModelChoiceField(queryset=Author.objects.all(), label='Author')
    tags = forms.CharField(widget=forms.Textarea, label='Tags')

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']
