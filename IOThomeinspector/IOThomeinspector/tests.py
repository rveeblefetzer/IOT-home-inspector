"""IOTehoeinspector test file."""


from django.test import TestCase
from .google_api import make_search
import bs4

class SearchResaultTestCase(TestCase):
    """Tests for the make search method."""

    def setUp(self):
        """Set up for test case."""
        self.soups = make_search('Philips hue')

    def test_soups_return(self):
        """Test that the soups list being returned is getting appended to."""
        self.assertTrue(len(self.soups) == 2)

    def test_type_of_items_in_soups_is_beautiful_soup(self):
        """Test that the items in the soups list getting returned are beautiful soup objects."""
        for soup in self.soups:
            self.assertTrue(type(soup) == bs4.BeautifulSoup)

    def test_getting_the_right_html_firmware(self):
        """Test that the html in the beautiful soup object contains the search resaults for firmware updates."""
        self.assertTrue(str(self.soups[0].title) == '<title>Philips hue firmware update - Bing</title>')

    def test_getting_the_right_html_security(self):
        """Test that the html in the beautiful soup object contains the search resaults for security vulnerabilities."""
        self.assertTrue(str(self.soups[1].title) == '<title>Philips hue security vulnerabilities - Bing</title>')

    def test_soups_is_list(self):
        """Test that make search returns a list."""
        self.assertTrue(type(self.soups) == list)

