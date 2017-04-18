from datetime import datetime

from django.conf import settings
from django.db import models


class Proposal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    description = models.CharField(max_length=500)
    # TODO: ATTACHMENT

    def __str__(self):
        return "title: " + str(self.title)

# class Category
