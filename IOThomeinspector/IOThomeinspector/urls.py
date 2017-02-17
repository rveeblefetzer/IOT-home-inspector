"""IOThomeinspector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from two_factor.admin import AdminSiteOTPRequired
from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete)
from django.views.static import serve
from django.conf.urls.static import static
from IOThomeinspector.views import HomePageView, team_view
from two_factor.urls import LoginView, SetupView

admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView, name='home'),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(
        regex=r'^account/login/$',
        view=LoginView.as_view(),
        name='login',
    ),
    url(
        regex=r'^account/two_factor/setup/$',
        view=SetupView.as_view(),
        name='setup',
    ),
    url(r'^registration/', include('registration.backends.hmac.urls')),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/', include('userprofile.urls')),
    url(r'^user/password/reset/$',
        password_reset,
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        password_reset_done),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect': '/user/password/done/'},
        name='password_reset_confirm'),
    url(r'^user/password/done/$',
        password_reset_complete),
    url(r'^team/$', team_view, name='team')
]
