from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^story/([0-9]+)/$', views.StoryView.as_view(), name='story'),
    url(r'^story/$', views.NewStoryView.as_view(), name='new_story'),
    url(r'^contribution/([0-9]+)/([0-9]+)/$', views.ContributionView.as_view(), name='contribution'),
    url(r'^', views.IndexView.as_view(), name="index"),
]
