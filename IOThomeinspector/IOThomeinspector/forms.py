from django import forms


class SearchForm(forms.BaseForm):
    """Form to edit profiles."""

    def __init__(self, *args, **kwargs):
        """Form fields."""
        super(SearchForm, self).__init__(*args, **kwargs)
        self.visible_fields["Search"] = forms.CharField(max_length=255)
