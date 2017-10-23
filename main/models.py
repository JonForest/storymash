from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=250)


class Contribution(models.Model):
    contribution_text = models.TextField()
    submitted_at = models.DateTimeField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE)