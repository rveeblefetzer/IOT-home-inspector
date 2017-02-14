"""User search using google."""


from bs4 import BeautifulSoup
import requests


def make_search(key_words):
    """Using the key words make a search request for new firmware."""
    soups = []
    extensions = ['+firmware+update', '+security+vulnerabilities', '+most+recent+version']
    for search_extension in extensions:
        search_term = '+'.join(key_words.split(' ')) + search_extension
        search_request = requests.get('https://bing.com/search?q=' + search_term, auth=('user', 'pass'))
        soup = BeautifulSoup(search_request.text, 'html.parser')
        soups.append(soup)
    return soups


def get_links(key_words):
    """Get the links we want to display to the user from our web search."""
    soups = make_search(key_words)
    filters = ['go.microsoft', 'blog']
    page_links = [[] for i in range(len(soups))]
    for soup in soups:
        for link in soup.find_all('a'):
            if 'http://' not in str(link.get('href')):
                pass
            elif 'blog' in str(link.get('href')):
                pass
            elif 'go.microsoft' in str(link.get('href')):
                pass
            else:
                page_links[soups.index(soup)].append(str(link.get('href')))
    return page_links
