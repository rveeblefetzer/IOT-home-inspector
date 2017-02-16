from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .models import UserProfile
import factory
from django.urls import reverse_lazy

"""Testing imports for 2 Factor Auth.
From https://github.com/Bouke/django-two-factor-auth/blob/master/tests/test_views_login.py."""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from django.test.utils import override_settings
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.oath import totp
from django_otp.util import random_hex
from .utils import UserMixin
try:
    from unittest import mock
except ImportError:
    import mock


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
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        response = HomePageView(req)
        self.assertTrue(response.status_code == 200)

    def test_home_view_status_is_ok2(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Chrome/56.3'
        response = HomePageView(req)
        self.assertTrue(
            'You are using Chrome/56.3, you are up to date!' in
            str(response.content))

    def test_home_view_status_is_ok3(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Firefox/56.3'
        response = HomePageView(req)
        self.assertTrue(
            'You are using Firefox/56.3, you are up to date!' in
            str(response.content))

    def test_home_view_status_is_ok4(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Safari/10.5'
        response = HomePageView(req)
        self.assertTrue(
            'You are using Safari/10.5, you are up to date!' in
            str(response.content))

    def test_home_view_status_is_ok5(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Chrome/50.3'
        response = HomePageView(req)
        self.assertTrue(
            'You are using Chrome/50.3, you are not up to date!' in
            str(response.content))

    def test_home_view_status_is_ok6(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Firefox/49'
        response = HomePageView(req)
        self.assertTrue(
            'You are using Firefox/49, you are not up to date!' in
            str(response.content))

    def test_home_view_status_is_ok7(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Safari/8'
        response = HomePageView(req)
        self.assertTrue(
            'You are using Safari/8, you are not up to date!' in
            str(response.content))

    def test_home_view_status_is_ok8(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        req.META['HTTP_USER_AGENT'] = 'Opera'
        response = HomePageView(req)
        self.assertTrue(
            "You are using Opera, we do not know if you are up to date!" in
            str(response.content))

    def test_home_view_status_is_ok9(self):
        """Test a get request on the home view."""
        from IOThomeinspector.views import HomePageView
        req = self.request.get("/")
        response = HomePageView(req)
        self.assertTrue('You are using' not in str(response.content))

    def test_home_route_uses_correct_templates(self):
        """Test that the correct templates are used on the home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_profile_page(self):
        """Test that login page loads corectly."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("profile"))
        self.assertTrue(response.status_code == 200)

    def test_search_page_not_logged_in(self):
        """Search should be ok whether logged in or not."""
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue('sf_links_titles' in response.context)

    def test_search_page_not_logged_in2(self):
        """Search should be ok whether logged in or not."""
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue(len(response.context['sf_links_titles']) > 0)

    def test_search_page_not_logged_in3(self):
        """Search should be ok whether logged in or not."""
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue('sec_links_titles' in response.context)

    def test_search_page_not_logged_in4(self):
        """Search should be ok whether logged in or not."""
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue(len(response.context['sec_links_titles']) > 0)

    def test_search_page_not_logged_in5(self):
        """Search should be ok whether logged in or not."""
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue('version' in response.context)

    def test_search_page_logged_in(self):
        """Search should be ok whether logged in or not."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue('sf_links_titles' in response.context)

    def test_search_page_logged_in2(self):
        """Search should be ok whether logged in or not."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue(len(response.context['sf_links_titles']) > 0)

    def test_search_page_logged_in3(self):
        """Search should be ok whether logged in or not."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue(len(response.context['sec_links_titles']) > 0)

    def test_search_page_logged_in4(self):
        """Search should be ok whether logged in or not."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('home'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue(
            'The most recent version number we could find' in
            response.context['version'])

    def test_search_profile_page_logged_in(self):
        """Search should be ok whether logged in or not."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('profile'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue('sec_links_titles' in response.context)

    def test_search_profile_page_logged_in2(self):
        """Search should be ok whether logged in or not."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('profile'),
                                    {'search': 'Philips Hue'},
                                    follow=True)
        self.assertTrue('version' in response.context)

    def test_edit_profile_page(self):
        """Test edit a profile."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.post(reverse_lazy('edit_profile'),
                                    {'Email': 'Philips@Hue.com'},
                                    follow=True)
        self.assertTrue(response.status_code == 200)

"""These are the 2 Factor Authorization tests from ."""


class LoginTest(UserMixin, TestCase):
    def _post(self, data=None):
        return self.client.post(reverse('two_factor:login'), data=data)

    def test_form(self):
        response = self.client.get(reverse('two_factor:login'))
        self.assertContains(response, 'Password:')

    def test_invalid_login(self):
        response = self._post({'auth-username': 'unknown',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertContains(response, 'Please enter a correct')
        self.assertContains(response, 'and password.')

    def test_valid_login_with_custom_redirect(self):
        redirect_url = reverse('two_factor:setup')
        self.create_user()
        response = self.client.post(
            '%s?%s' % (reverse('two_factor:login'), 'next=' + redirect_url),
            {'auth-username': 'bouke@example.com',
             'auth-password': 'secret',
             'login_view-current_step': 'auth'})
        self.assertRedirects(response, redirect_url)

    def test_login_enables_profile_view(self):
        """Test that a logged-in user can access profile view."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.get('/profile/')
        self.assertIn(b"You are logged in as", response.content)

    def test_not_logged_in_enables_no_profile_view(self):
        """Test that user can't access profile view without logging in."""
        response = self.client.get('/profile/')
        self.assertNotIn(b"You are logged in as", response.content)
###
    def test_login_editing_profile_redirects_to_profile(self):
        """Test that a profile edit 302s to profile view."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('profile'))
        self.assertTrue(response.status_code == 200)

    def test_valid_login_with_custom_redirect(self):
        redirect_url = reverse('two_factor:setup')
        self.create_user()
        response = self.client.post(
            '%s?%s' % (reverse('two_factor:login'), 'next=' + redirect_url),
            {'auth-username': 'bouke@example.com',
             'auth-password': 'secret',
             'login_view-current_step': 'auth'})
        self.assertRedirects(response, redirect_url)

    @mock.patch('two_factor.views.core.signals.user_verified.send')
    def test_with_generator(self, mock_signal):
        user = self.create_user()
        device = user.totpdevice_set.create(name='default',
                                            key=random_hex().decode())

        response = self._post({'auth-username': 'bouke@example.com',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertContains(response, 'Token:')

        response = self._post({'token-otp_token': '123456',
                               'login_view-current_step': 'token'})
        self.assertEqual(response.context_data['wizard']['form'].errors,
                         {'__all__': ['Invalid token. Please make sure you '
                                      'have entered it correctly.']})

        response = self._post({'token-otp_token': totp(device.bin_key),
                               'login_view-current_step': 'token'})
        self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        self.assertEqual(device.persistent_id,
                         self.client.session.get(DEVICE_ID_SESSION_KEY))

        # Check that the signal was fired.
        mock_signal.assert_called_with(sender=mock.ANY, request=mock.ANY, user=user, device=device)


    @mock.patch('two_factor.views.core.signals.user_verified.send')
    def test_with_backup_token(self, mock_signal):
        user = self.create_user()
        user.totpdevice_set.create(name='default', key=random_hex().decode())
        device = user.staticdevice_set.create(name='backup')
        device.token_set.create(token='abcdef123')

        # Backup phones should be listed on the login form
        response = self._post({'auth-username': 'bouke@example.com',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertContains(response, 'Backup Token')

        # Should be able to go to backup tokens step in wizard
        response = self._post({'wizard_goto_step': 'backup'})
        self.assertContains(response, 'backup tokens')

        # Wrong codes should not be accepted
        response = self._post({'backup-otp_token': 'WRONG',
                               'login_view-current_step': 'backup'})
        self.assertEqual(response.context_data['wizard']['form'].errors,
                         {'__all__': ['Invalid token. Please make sure you '
                                      'have entered it correctly.']})

        # Valid token should be accepted.
        response = self._post({'backup-otp_token': 'abcdef123',
                               'login_view-current_step': 'backup'})
        self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        # Check that the signal was fired.
        mock_signal.assert_called_with(sender=mock.ANY, request=mock.ANY, user=user, device=device)

    @mock.patch('two_factor.views.utils.logger')
    def test_change_password_in_between(self, mock_logger):
        """
        When the password of the user is changed while trying to login, should
        not result in errors. Refs #63.
        """
        user = self.create_user()
        self.enable_otp()

        response = self._post({'auth-username': 'bouke@example.com',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertContains(response, 'Token:')

        # Now, the password is changed. When the form is submitted, the
        # credentials should be checked again. If that's the case, the
        # login form should note that the credentials are invalid.
        user.set_password('secret2')
        user.save()
        response = self._post({'login_view-current_step': 'token'})
        self.assertContains(response, 'Please enter a correct')
        self.assertContains(response, 'and password.')

        # Check that a message was logged.
        mock_logger.warning.assert_called_with(
            "Current step '%s' is no longer valid, returning to last valid "
            "step in the wizard.",
            'token')

    @mock.patch('two_factor.views.utils.logger')
    def test_reset_wizard_state(self, mock_logger):
        self.create_user()
        self.enable_otp()

        response = self._post({'auth-username': 'bouke@example.com',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertContains(response, 'Token:')

        # A GET request resets the state of the wizard...
        self.client.get(reverse('two_factor:login'))

        # ...so there is no user in this request anymore. As the login flow
        # depends on a user being present, this should be handled gracefully.
        response = self._post({'token-otp_token': '123456',
                               'login_view-current_step': 'token'})
        self.assertContains(response, 'Password:')

        # Check that a message was logged.
        mock_logger.warning.assert_called_with(
            "Requested step '%s' is no longer valid, returning to last valid "
            "step in the wizard.",
            'token')

    @mock.patch('two_factor.views.utils.logger')
    def test_login_different_user_on_existing_session(self, mock_logger):
        """
        This test reproduces the issue where a user is logged in and a different user
        attempts to login.
        """
        self.create_user()
        self.create_user(username='vedran@example.com')

        response = self._post({'auth-username': 'bouke@example.com',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        response = self._post({'auth-username': 'vedran@example.com',
                               'auth-password': 'secret',
                               'login_view-current_step': 'auth'})
        self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))


class BackupTokensTest(UserMixin, TestCase):
    def setUp(self):
        super(BackupTokensTest, self).setUp()
        self.create_user()
        self.enable_otp()
        self.login_user()

    def test_empty(self):
        response = self.client.get(reverse('two_factor:backup_tokens'))
        self.assertContains(response, 'You don\'t have any backup codes yet.')

    def test_generate(self):
        url = reverse('two_factor:backup_tokens')

        response = self.client.post(url)
        self.assertRedirects(response, url)

        response = self.client.get(url)
        first_set = set([token.token for token in
                        response.context_data['device'].token_set.all()])
        self.assertNotContains(response, 'You don\'t have any backup codes '
                                         'yet.')
        self.assertEqual(10, len(first_set))

        # Generating the tokens should give a fresh set
        self.client.post(url)
        response = self.client.get(url)
        second_set = set([token.token for token in
                         response.context_data['device'].token_set.all()])
        self.assertNotEqual(first_set, second_set)
