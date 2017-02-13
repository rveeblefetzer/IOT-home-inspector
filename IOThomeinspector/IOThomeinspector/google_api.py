"""User search using google."""


from bs4 import BeautifulSoup
import requests


def make_search(key_words):
    """Using the key words make a search request for new firmware."""
    soups = []
    extensions = ['+firmware+update', '+security+vulnerabilities']
    for search_extension in extensions:
        print('https://bing.com/search?q=' + '+'.join(key_words.split(' ')) + search_extension)
        search_term = '+'.join(key_words.split(' ')) + search_extension
        search_request = requests.get('https://bing.com/search?q=' + search_term, auth=('user', 'pass'))
        soup = BeautifulSoup(search_request.text, 'html.parser')
        soups.append(soup)
    return soups
