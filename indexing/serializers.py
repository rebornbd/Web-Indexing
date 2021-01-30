from rest_framework import serializers
from .models import WIModel

def wi_link_serializer(links, title, desc):
  mylinks = []
  for link in links:
    mylinks.append(link)
  
  return [{'title': title, 'desc': desc, 'links': [mylinks]}]

class WISerializer(serializers.ModelSerializer):
  class Meta:
    model = WIModel
    fields = '__all__'