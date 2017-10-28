from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^story/([0-9]+)/$', views.StoryView.as_view(), name='story'),
    url(r'^story/$', views.NewStoryView.as_view(), name='new_story'),
    url(r'^', views.IndexView.as_view(), name="index"),
]
