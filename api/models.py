
from django.conf import settings
from django.db import models
from django.utils import timezone


class Proposal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField(default=timezone.now, blank=True, null=True)
    description = models.CharField(max_length=500)
    articles = models.IntegerField(default=0)
    discussions = models.IntegerField(default=0)
    # TODO: ATTACHMENT

    def __str__(self):
        return "title: " + str(self.title)


class Category(models.Model):
    source = models.CharField(max_length=200)

    def __str__(self):
        return "source: " + str(self.source)
