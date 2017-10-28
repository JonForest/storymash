from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^story/([0-9]+)/$', views.story, name='story'),
    url(r'^story/$', views.new_story, name='new_story'),
    url(r'^', views.IndexView.as_view(), name="index"),
]
