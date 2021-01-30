from .models import WIModel

import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlparse, urljoin


# web crawling
def webIndexingTask(url):
  if (url_validator(url)):
    links = set()

    try:
      response = requests.get(url)
      soup = BeautifulSoup(response.content, "html.parser")

      for link in soup.find_all('a', href=True):
        mylink = str(link.get('href'))
        myurl = urljoin(url, mylink)

        if (url_validator(myurl)):
          links.add(myurl)
        
        mylinks     = list(links)
        parse_links = json.dumps(mylinks)
        
        widatas = WIModel.objects.filter(link=str(url))

        if (len(widatas) > 0):
          for i in range(0, len(widatas)):
            wi = widatas[i]
            wi.parse_links = parse_links
            wi.save()
        
        else:
          wi = WIModel(link=str(url), parse_links=parse_links, title='title', description='description')
          wi.save()
    
    except Exception as e:
      print(e)


# check url validity
def url_validator(url):
  try:
    result = urlparse(url)
    # return all([result.scheme, result.netloc, result.path])
    return all([result.scheme, result.netloc])
        
  except:
    return False
