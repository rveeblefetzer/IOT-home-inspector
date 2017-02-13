"""Creating Models for user profile."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
import uuid

DEVICE_CHOICES = (
    ("philips-hue", "Philips Hue"),
    ("amazon-echo", "Amazon Echo"),
    ("nest", "Nest"),
    ("fitbit", "FitBit")
)

class ActiveUserManager(models.Manager):
    """Query UserProfile of active user."""

    def get_queryset(self):
        """Return query set of profiles for active users."""
        query = super(ActiveUserManager, self).get_queryset()
        return query.filter(user__is_active__exact=True)


class UserProfile(models.Model):
    """Creating profile linked to user."""

    user = models.OneToOneField( # Association user class and profile class
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )

    devices = MultiSelectField(choices=DEVICE_CHOICES)
    userprofile_id = models.UUIDField(default=uuid.uuid4, editable=False)
    active = ActiveUserManager()
    objects = models.Manager()

    def __str__(self):
        return self.user.username

    @property
    def is_active(self):
        """This is active property."""
        return self.user.is_active


@receiver(post_save, sender=User)
def make_user_profile(sender, instance, **kwargs):
    """Instantiate a UserProfile, connect to a new User instance, save that profile."""
    if kwargs["created"]:
        new_profile = UserProfile(user=instance)
        new_profile.save()


# # Class for another app to implement two-factor auth. This sets a device for time-based one-time pad
# class django_otp.plugins.otp_totp.models.TOTPDevice():
#     user = models.OneToOneField(settings.AUTH_USER_MODEL)
