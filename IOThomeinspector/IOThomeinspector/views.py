"""Views for Home Page."""
from userprofile.models import UserProfile
from django.conf import settings
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Return the Home View inheriting from TemplateView."""

    template_name = 'home.html'

    def get_context_data(self):
        """View for the home page."""
        try:
            ua_profile = self.request.META['HTTP_USER_AGENT'].split()
            check = True
            for item in ua_profile:
                if "Chrome" in item:
                    browser = item
                    if float(browser.split('/')[1][0:4]) < 56:
                        check = False
                    break
                elif "Firefox" in item:
                    browser = item
                    if float(browser.split('/')[1][0:4]) < 51:
                        check = False
                    break
                elif "Safari" in item:
                    browser = item
                    if float(browser.split('/')[1][0:4]) < 10:
                        check = False
                else:
                    browser = None
            if check is True:
                browser = "You are using " + browser + ", you are up to date!"
            else:
                browser = "You are using " + browser + ", you are not up to date!"
            if browser:
                context = {'browser': browser}
                # import pdb; pdb.set_trace()
                return context
        except KeyError:
            return {}
