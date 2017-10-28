from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import generic

from .models import Story, Contribution
from django.utils.html import strip_tags


# Example of a class-based view
class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'latest_stories'

    def get_queryset(self):
        """Return all the stories"""
        return Story.objects.all()


def story(request, story_id):
    found_story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
    if not len(found_story):
        raise Http404('No Story matches the provided id.')

    if request.method == 'GET':
        return render(request, 'main/story.html', {'story': found_story.first()})
    elif request.method == 'POST':
        contribution_text = strip_tags(request.POST['contribution_text'])
        contribution = Contribution(contribution_text=contribution_text, story_id=story_id)
        contribution.save()

        # Fetch story again with any updates
        refreshed_story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
        return render(request, 'main/story.html', {'story': refreshed_story.first()})
    else:
        raise HttpResponse('{} not supported'.format(request.method,), status=500)


def new_story(request):
    if request.method == 'GET':
        return render(request, 'main/new_story.html')
    elif request.method == 'POST':
        title = strip_tags(request.POST['title'])
        new_user_story = Story(title=title)
        new_user_story.save()

        return redirect('index')
    else:
        raise HttpResponse('{} not supported'.format(request.method,), status=500)