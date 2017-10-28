from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contribution(models.Model):
    contribution_text = models.TextField()
    submitted_at = models.DateTimeField(default=datetime.now)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.contribution_text
