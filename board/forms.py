from django import forms
from .models import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ('author', 'slug', 'status', 'views', 'created_at', 'updated_at')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
            'tags': forms.SelectMultiple(attrs={'size': 5}),
        }