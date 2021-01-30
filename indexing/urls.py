from django.urls import path
from . import views

# template tagging
app_name = 'web_indexing'

urlpatterns = [
    path('', views.WIList.as_view(), name='list'),
]
