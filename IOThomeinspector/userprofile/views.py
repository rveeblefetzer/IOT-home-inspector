"""Views for the User Profile."""

from userprofile.forms import EditProfileForm
from django.conf import settings
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import redirect


class ProfileView(TemplateView):
    """Return the Profile View inheriting from TemplateView."""

    template_name = 'userprofile/profile.html'

    def get_context_data(self, username=None):
        """Get profiles and return them."""
        if self.request.user.is_authenticated():
            profile = self.request.user.profile
            devices = profile.get_devices_display().split(',')
            return {'profile': profile, 'devices': devices}
        else:
            error_message = "You're not signed in."
            return {'error': error_message}


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Edit the authenticated users profile."""

    template_name = 'userprofile/edit_profile.html'
    model = UserProfile
    form_class = EditProfileForm

    def get_object(self):
        """Get the user profile object."""
        return self.request.user.profile

    def form_valid(self, form):
        """Save model forms to database."""
        self.object = form.save()
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.profile.devices = form.cleaned_data['devices']
        self.object.user.save()
        self.object.save()
        return redirect('profile')