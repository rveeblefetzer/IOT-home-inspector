"""User search using google."""


import webbrowser


def make_search(key_words):
  """Using the key words make a search request for new firmware."""
  base_url = 'https://google.com/#q='
  search_term = '+'.join(key_words.split(' ')) + '+firmware+update'
  search = base_url + search_term
  webbrowser.open(search, new=0, autoraise=True)