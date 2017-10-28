from django.http import Http404
from django.core.exceptions import PermissionDenied
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
        contribution = Contribution(contribution_text=contribution_text, story_id=story_id, author=request.user)
        contribution.save()

        # Fetch story again with any updates
        refreshed_story = Story.objects.prefetch_related('contribution_set').filter(id=story_id)
        return render(request, 'main/story.html', {'story': refreshed_story.first()})


@method_decorator(login_required, name='dispatch')
class ContributionView(generic.DetailView):
    def get(self, request, *args, **kwargs):
        [story_id, contribution_id] = args
        try:
            story, contribution = self._get_story_contribution(request.user, story_id, contribution_id)
            return render(request, 'main/contribution.html', {'story': story, 'contribution': contribution})
        except PermissionDenied:
            return redirect('story', story_id)

    def post(self, request, *args):
        [story_id, contribution_id] = args
        contribution_text = strip_tags(request.POST['contribution_text'])
        try:
            story, contribution = self._get_story_contribution(request.user, story_id, contribution_id)
        except PermissionDenied:
            return redirect('story', story_id)

        contribution.contribution_text = contribution_text
        contribution.save()

        return redirect('story', story.id)

    def _get_story_contribution(self, author, story_id, contribution_id):
        found_story = Story.objects.filter(id=story_id)
        found_contribution = Contribution.objects.filter(id=contribution_id)
        if not len(found_story):
            raise Http404('No Story matches the provided id.')

        if not len(found_contribution):
            raise Http404('No Contribution matches the provided id.')

        if found_contribution.first().author != author:
            raise PermissionDenied

        return found_story.first(), found_contribution.first()



@method_decorator(login_required, name='dispatch')
class NewStoryView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'main/new_story.html')

    def post(self, request):
        title = strip_tags(request.POST['title'])
        new_user_story = Story(title=title, author=request.user)
        new_user_story.save()

        return redirect('index')