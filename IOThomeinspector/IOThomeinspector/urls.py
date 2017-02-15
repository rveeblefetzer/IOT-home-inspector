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
from django.contrib.auth.views import logout
from django.views.static import serve
from django.conf.urls.static import static
from IOThomeinspector.views import HomePageView
from two_factor.urls import LoginView, SetupView

admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(), name='home'),
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
    url(r'^profile/', include('userprofile.urls'))
]
