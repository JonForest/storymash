from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^story/([0-9]+)/$', views.view_story, name='story'),
    url(r'^', views.index),
]
