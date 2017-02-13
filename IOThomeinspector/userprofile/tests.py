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
        # import pdb; pdb.set_trace()
        self.assertTrue(len(test_user.profile.devices) == 2)
