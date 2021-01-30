from django.shortcuts import render

from .models import WIModel
import json
from .tasks import url_validator, webIndexingTask

def WebIndexingListView(request):
  context = {}

  url = request.GET.get('link')

  # print("######: " + url + " :#####")

  if (url_validator(url) and len(url)>5):
    # print("######: " + url + " :#####")

    if (URLNotExists(url)):
      print("######: " + url + " :#####")
      webIndexingTask(url)

      results = url_filter(url)
      if (len(results)> 0):
        mylinks = results[0].parse_links
        links = json.loads(mylinks)
        context["links"] = links

    else:
      results = url_filter(url)
      if (len(results)> 0):
        mylinks = results[0].parse_links
        links = json.loads(mylinks)
        context["links"] = links

  else:
    context["links"] = ["enter a valid urls"]
  
  return render(request, 'indexing/list.html', context=context)


# url not exists
def URLNotExists(url):
  qs = url_filter(url)

  if (len(qs) > 0):
    return False
  return True

def url_filter(url):
  return WIModel.objects.filter(link=str(url))
