"""Custome forms file."""


from django import forms
from .google_api import get_links


class MakeSearchForm(forms.Form):
    """Subit a search."""
    search = forms.CharField()
    links = get_links(str(search))