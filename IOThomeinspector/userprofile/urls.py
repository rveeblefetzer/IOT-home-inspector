from django.conf.urls import url
from userprofile.views import (
    EditProfileView,
    ProfileView,
)


urlpatterns = [
    url(r'^edit$', EditProfileView.as_view(), name='edit_profile'),
    url(r'^$', ProfileView.as_view(), name="profile"),
]
