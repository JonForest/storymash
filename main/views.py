from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Story, Contribution
from django.utils.html import strip_tags


# Example of a class-based view
class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'latest_stories'

    def get_queryset(self):
        """Return all the stories"""
        return Story.objects.all()


@method_decorator(login_required, name='post')
class StoryView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        story_id = args[0]
        found_story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
        if not len(found_story):
            raise Http404('No Story matches the provided id.')

        return render(request, 'main/story.html', {'story': found_story.first()})

    def post(self, request, *args):
        story_id = args[0]
        found_story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
        if not len(found_story):
            raise Http404('No Story matches the provided id.')

        contribution_text = strip_tags(request.POST['contribution_text'])
        contribution = Contribution(contribution_text=contribution_text, story_id=story_id)
        contribution.save()

        # Fetch story again with any updates
        refreshed_story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
        return render(request, 'main/story.html', {'story': refreshed_story.first()})


@method_decorator(login_required, name='dispatch')
class NewStoryView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'main/new_story.html')

    def post(self, request):
        title = strip_tags(request.POST['title'])
        new_user_story = Story(title=title)
        new_user_story.save()

        return redirect('index')