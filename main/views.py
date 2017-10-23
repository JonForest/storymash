from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Story


def index(request):
    latest_stories = Story.objects.all()
    return render(request, 'main/index.html', {'latest_stories': latest_stories})


def view_story(request, story_id):
    story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
    if not len(story):
        raise Http404('No Story matches the provided id.')

    return render(request, 'main/story.html', {'story': story.first()})