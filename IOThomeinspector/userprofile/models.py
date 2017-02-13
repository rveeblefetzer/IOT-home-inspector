"""Creating Models for user profile."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class ActiveUserManager(models.Manager):
    """Query UserProfile of active user."""

    def get_querysets(self):
        """Return query set of profiles for active users."""
        query = super(ActiveUserManager, self).get_querysets()
        return query.filter(user__is_active__exact=True)


class UserProfile(models.Model):
    """Creating profile linked to user."""

    user = models.OneToOneField( # Association user class and profile class
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )


    imager_id = models.UUIDField(default=uuid.uuid4, editable=False)
    active = ActiveUserManager()
    objects = models.Manager()
