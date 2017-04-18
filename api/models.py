from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Proposal(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    description = models.CharField(max_length=500)
    # TODO: ATTACHMENT

    def __str__(self):
        return "title: " + str(self.title)

# class Category
