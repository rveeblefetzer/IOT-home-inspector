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


def get_links(key_words):
    """Get the links we want to display to the user from our web search."""
    soups = make_search(key_words)
    filters = ['go.microsoft', 'blog']
    page_links = [[] for i in len(soups)]
    for soup in soups:
        for link in soup.find_all('a'):
            if 'http://' in str(link.get('href')) and 'blog' not in str(link.get('href')) and 'go.microsoft' not in str(link.get('href')):
                page_links[soups.index(soup)].append(str(link.get('href')))
    return page_links
