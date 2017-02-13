from django.test import TestCase, Client, RequestFactory
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

    # tests for registration and login

class ProfileLoginRegisterTests(TestCase):
    """Tests for user profile front end, registering and logging in."""

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()

    def register_new_user(self, follow=True):
        """New user fixture."""
        return self.client.post("/registration/register/", {
            "username": "Jerry",
            "email": "jerry@reed.com",
            "password1": "tugboats",
            "password2": "tugboats"
        }, follow=follow)

    def test_home_view_status_is_ok(self):
        """Test a get request on the HomePageView."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        view = HomePageView.as_view()
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_home_route_uses_correct_templates(self):
        """Test that the correct templates are used on the home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_login_route_is_status_ok(self):
        """Test for a 200 status route at /login."""
        response = self.client.get("/login/")
        self.assertTrue(response.status_code == 200)

    def test_login_route_redirects(self):
        """Login route redirect?."""
        new_user = UserFactory.create()
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"
        }, follow=False)
        self.assertTrue(response.status_code == 302)

    def test_login_route_redirects_to_home(self):
        """Login route redirect to homepage?."""
        new_user = UserFactory.create()
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"}, follow=True)
        self.assertTrue(response.redirect_chain[0][0] == '/')

