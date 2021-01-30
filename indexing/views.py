from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import WIModel
from .serializers import wi_link_serializer
import json
from .tasks import url_validator, webIndexingTask


class WIList(APIView):
  def get(self, request):
    url = request.query_params.get('url')
    serialize = []
    if (url_validator(url) and len(url)>5):
      if (URLNotExists(url)):
        webIndexingTask(url)

        results = url_filter(url)
        if (len(results)> 0):
          mylinks = results[0].parse_links
          links = json.loads(mylinks)
          serialize = wi_link_serializer(links, title, desc)
      
      else:
        results = url_filter(url)
        if (len(results)> 0):
          title   = results[0].title
          desc    = results[0].description
          mylinks = results[0].parse_links
          links   = json.loads(mylinks)
          serialize = wi_link_serializer(links, title, desc)
    else:
      serialize = {"error": "enter valid url"}

    return Response(serialize)

def WebIndexingListView(request):
  context = {}

  url = request.GET.get('link')
  if (url_validator(url) and len(url)>5):
    if (URLNotExists(url)):
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
