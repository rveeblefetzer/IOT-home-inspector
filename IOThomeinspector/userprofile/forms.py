from django import forms
from .models import UserProfile


class EditProfileForm(forms.ModelForm):
    """Form to edit profiles."""

    def __init__(self, *args, **kwargs):
        """Form fields."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["Email"] = forms.EmailField(initial=self.instance.user.email)

    class Meta:
        """Exclusion principles."""
        model = UserProfile
        fields = ['devices']
