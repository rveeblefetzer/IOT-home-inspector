"""Views for Home Page."""
from userprofile.models import UserProfile
from django.conf import settings
from django.views.generic import TemplateView
from .google_api import get_links
from django.http import HttpResponseRedirect
from django.shortcuts import render

def HomePageView(request):
    """Return the Home View ."""
    if request.method == "POST":
        keywords = request.POST['search']
        makelist = get_links(keywords)
        kwcontext = []
        for sublist in makelist:
            for item in sublist:
                kwcontext.append(item)
        return render(request, 'home.html', {"kwcontext": kwcontext})
    try:
        ua_profile = request.META['HTTP_USER_AGENT'].split()
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
            return render(request, 'home.html', context)
    except KeyError:
        context = {}
        return render(request, 'home.html', context)
