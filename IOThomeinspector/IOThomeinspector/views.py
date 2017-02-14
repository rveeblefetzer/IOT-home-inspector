"""Views for Home Page."""
from userprofile.models import UserProfile
from django.conf import settings
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Return the Home View inheriting from TemplateView."""

    template_name = 'home.html'

    def get_context_data(self):
        """View for the home page."""
        context = {}
        return context
