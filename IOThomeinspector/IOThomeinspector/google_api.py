"""User search using google."""


from bs4 import BeautifulSoup
import requests


def make_search(key_words):
    """Takes user input as a string and returns a list of beautiful soup objects for each search extension in the extensions list."""
    key_words = key_words.lower()
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
    key_words = key_words.lower()
    links = []
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
                page_links[soups.index(soup)].append((str(link.get('href')),str(link.get_text())))
                if soup is soups[2]:
                    links.append(link)
    version_number = 'The most recent version number we could find is ' + get_versions(key_words, links)
    return (page_links[:2], version_number)


def get_versions(key_words, links):
    """Try to find the most recent versions of firmware bsed on the relevent links."""
    key_words = key_words.lower()
    soup = None
    top_links = [
                'http://www2.meethue.com/en-us/release-notes/bridge/',
                'https://www.amazon.com/gp/help/customer/display.html/ref=as_li_ss_tl?nodeId=201602210&linkCode=ll2&tag=lovemyecho-20&linkId=0ce46b6aac3da632049edf10ad05bffd',
    ]
    #check to see if what the user is searching for is an item we have acounted for and if it is return the most recents version number from its page.
    if 'philips' in key_words and 'hue' in key_words:
        soup = BeautifulSoup(requests.get(top_links[0], auth=('user', 'pass')).text, 'html.parser')
    elif 'amazon' in key_words and 'echo' in key_words:
        soup = BeautifulSoup(requests.get(top_links[1], auth=('user', 'pass')).text, 'html.parser')
    if soup:
        return scrape_soup(key_words, soup)
    #if the user is not searching for something we acounted for we search through all the relavent links and find what we believe to be the most recent version number.
    for link in links:
        soup = BeautifulSoup(requests.get(link.get('href'), auth=('user', 'pass')).text, 'html.parser')
        if scrape_soup(key_words, soup) != 'We could not find the most recent software/firmware version of you device, hopefully these links will help.':
            return scrape_soup(key_words, soup)
    return scrape_soup(key_words, soup)
        

def scrape_soup(key_words, soup):
    """Scrape the soup for the most recent version number"""
    key_words = key_words.lower()
    hot_words = ['version:', 'Version:', 'version', 'Version', 'firmware', 'software', 'Firmware', 'Software']
    highest_priority_val = 0
    highest_priority_num = ''
    for word in key_words.split(' '):
        hot_words.append(word)
    probable_numbers = {}
    page_text = soup.get_text()
    page_text = page_text.replace('\n', ' ')
    page_text = page_text.split(' ')
    page_text = [x for x in page_text if x != '']
    for word in page_text:
        try:
            if word == '':
                continue
            elif type(int(word[0])) is int and type(int(word[-1])) is int:
                probable_numbers[word] = 0
                for index in page_text[page_text.index(word) - 5:page_text.index(word)]:
                    for hword in hot_words:
                        if hword in index:
                            probable_numbers[word] += 1
        except ValueError:
            continue
    for num in probable_numbers.keys():
        try:
            if probable_numbers[num] > highest_priority_val:
                highest_priority_val = probable_numbers[num]
                highest_priority_num = num
            elif probable_numbers[num] == highest_priority_val:
                compare_new = num.split('.')
                compare_curr = highest_priority_num.split('.')
                for index_compare in range(len(compare_new)):
                    try:
                        if int(compare_new[index_compare]) > int(compare_curr[index_compare]):
                            highest_priority_val = probable_numbers[num]
                            highest_priority_num = num
                    except IndexError:
                        highest_priority_val = probable_numbers[num]
                        highest_priority_num = num
        except ValueError:
            continue
    if highest_priority_num == '':
        return 'We could not find the most recent software/firmware version of you device, hopefully these links will help. If you want to search again try being more specific.'
    return highest_priority_num