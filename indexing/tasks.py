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
          links.add(mylink)
        
        mylinks     = list(links)
        parse_links = json.dumps(mylinks)
        
        widatas = WIModel.objects.filter(link=str(url))

        if (len(widatas) > 0):
          for i in range(0, len(widatas)):
            wi = widatas[i]
            wi.parse_links = parse_links
            wi.save()
        
        else:
          title, desc = title_desc(url)
          wi = WIModel(link=str(url), parse_links=parse_links, title=title, description=desc)
          wi.save()
    
    except Exception as e:
      print(e)


def title_desc(url):
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = getTitle(soup.title.text, url)
    desc  = soup.text[:1000]

    return title, desc

  except Exception as e:
    print(e)


def getTitle(title, url):
  if (title == "" or title == None):
    domain = urlparse(url).netloc
    return domain
  return title[:150]

def getDesc():
  pass

# check url validity
def url_validator(url):
  try:
    result = urlparse(url)
    # return all([result.scheme, result.netloc, result.path])
    return all([result.scheme, result.netloc])
        
  except:
    return False
