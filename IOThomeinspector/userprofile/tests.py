from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(
        lambda number: "{} bob".format(number)
    )
    email = factory.LazyAttribute(
        lambda x: "{}@gmail.com".format(x.username)
    )


class ProfileTestCase(TestCase):
    """Profile Model being test with this class."""

    def setUp(self):
        """Setup profile to test."""
        self.users = [UserFactory.create() for i in range(20)]

    def test_reciever(self):
        """Test new users are made for profile."""
        self.assertEqual(UserProfile.objects.count(), 20)

    def test_user_has_profile_attached(self):
        """Testing for Profiles attached Users."""
        bob = self.users[2]
        self.assertTrue(hasattr(bob, "profile"))
        self.assertIsInstance(bob.profile, UserProfile)

    def test_profile_associated_actual_users(self):
        """Testing for profile Associated with real users."""
        a_profile = UserProfile.objects.first()
        self.assertTrue(hasattr(a_profile, "user"))
        self.assertIsInstance(a_profile.user, User)

    def test_profile_str_is_user_username(self):
        """Testing profile _str_ is username."""
        profile = UserProfile.objects.get(user=self.users[0])
        self.assertEqual(str(profile), self.users[0].username)

    def test_user_profile_has_devices(self):
        """Testing user profile has devices."""
        profile = UserProfile.objects.get(user=self.users[0])
        profile.devices = "nest"
        profile.save()
        test_user = User.objects.filter(username=profile.user.username).first()
        self.assertTrue(test_user.profile.devices == [profile.devices])

    def test_user_profile_has_multiple_devices(self):
        """Testing user profile has devices."""
        profile = UserProfile.objects.get(user=self.users[0])
        profile.devices = ["nest", "amazon-echo"]
        profile.save()
        test_user = User.objects.filter(username=profile.user.username).first()
        self.assertTrue(len(test_user.profile.devices) == 2)

    def test_user_is_active(self):
        """User should be active."""
        user = self.users[0]
        self.assertTrue(user.is_active)

    def test_user_is_active2(self):
        """User should be active."""
        user = self.users[0]
        self.assertTrue(user.profile.is_active)

    def test_inactive_users(self):
        """Test that inactive users are not active."""
        the_user = self.users[0]
        the_user.is_active = False
        the_user.save()
        self.assertTrue(UserProfile.active.count() == User.objects.count() - 1)

    def test_delete_user_deletes_profile(self):
        """Deleting a user should delete a profile associated with it."""
        user = self.users[0]
        self.assertTrue(UserProfile.objects.count() == 20)
        count = UserProfile.objects.count()
        user.delete()
        self.assertTrue(UserProfile.objects.count() == count - 1)

    def test_delete_user_deletes_user(self):
        """Deleting a user should delete the user."""
        user = self.users[0]
        count = User.objects.count()
        user.delete()
        self.assertTrue(User.objects.count() == count - 1)