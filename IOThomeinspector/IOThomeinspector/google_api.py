"""User search using google."""


from bs4 import BeautifulSoup
import requests


def make_search(key_words):
    """Takes user input as a string and returns a list of beautiful soup objects for each search extension in the extensions list."""
    soups = []
    extensions = ['+firmware+update', '+security+vulnerabilities', '+most+recent+firmware+version']
    for search_extension in extensions:
        search_term = '+'.join(key_words.split(' ')) + search_extension
        search_request = requests.get('https://bing.com/search?q=' + search_term, auth=('user', 'pass'))
        soup = BeautifulSoup(search_request.text, 'html.parser')
        soups.append(soup)
    return soups


def get_links(key_words):
    """Takes in user input as key words and returns a list containnig lists of relevent links from each extension in the function above.."""
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


def get_versions(key_words, links=None):
    """Try to find the most recent versions of firmware bsed on the relevent links."""
    import pdb; pdb.set_trace()
    soup = None
    top_links = [
                'http://www2.meethue.com/en-us/release-notes/bridge/'
                'https://nest.com/support/article/Nest-Learning-Thermostat-software-update-history',
                'https://nest.com/support/article/Nest-Cam-and-Dropcam-software-update-history',
                'https://nest.com/support/article/Nest-Protect-software-update-history',
                'https://www.amazon.com/gp/help/customer/display.html/ref=as_li_ss_tl?nodeId=201602210&linkCode=ll2&tag=lovemyecho-20&linkId=0ce46b6aac3da632049edf10ad05bffd',
    ]
    #check to see if what the user is searching for is an item we have acounted for and if it is return the most recents version number from its page.
    if 'philips' in key_words.lower() and 'hue' in key_words.lower():
        soup = BeautifulSoup(requests.get(top_links[0], auth=('user', 'pass')).text, 'html.parser')
    elif 'nest' in key_words.lower() and 'thermostat' in key_words.lower():
        soup = BeautifulSoup(requests.get(top_links[1], auth=('user', 'pass')).text, 'html.parser')
    elif 'nest' in key_words.lower() and 'dropcam' in key_words.lower():
        soup = BeautifulSoup(requests.get(top_links[2], auth=('user', 'pass')).text, 'html.parser')
    elif 'nest' in key_words.lower() and 'protect' in key_words.lower():
        soup = BeautifulSoup(requests.get(top_links[3], auth=('user', 'pass')).text, 'html.parser')
    elif 'amazon' in key_words.lower() and 'echo' in key_words.lower():
        soup = BeautifulSoup(requests.get(top_links[4], auth=('user', 'pass')).text, 'html.parser')
    if soup:
        return scrape_soup(key_words, soup)
    #if the user is not searching for something we acounted for we search through all the relavent links and find what we believe to be the most recent version number.
    for link in links:
        soup = BeautifulSoup(requests.get(link, auth=('user', 'pass')).text, 'html.parser')
        if scrape_soup(key_words, soup) != 'We could not find the most recent software/firmware version of you device, hopefully these links will help.':
            return scrape_soup(key_words, soup)
    return scrape_soup(key_words, soup)
        

def scrape_soup(key_words, soup):
    """Scrape the soup for the most recent version number"""
    hot_words = ['version:', 'Version:', 'version', 'Version', 'V', 'v', 'firmware', 'software', 'Firmware', 'Software']
    elements = soup.find_all()
    flags = [0 for i in elements]
    for element in elements:
        for word in hot_words:
            if word in str(element):
                for kword in key_words.split(' '):
                    if kword.lower() in str(element).lower():
                        flags[elements.index(element)] += 1
    element = elements[flags.index(max(flags))]
    element = str(element).split(' ')
    try:
        if int(element[element.index(word) + 1][0]):
            return str(element[element.index(word) + 1])
    except ValueError:
        return 'We could not find the most recent software/firmware version of you device, hopefully these links will help.'