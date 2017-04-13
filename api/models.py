from django.db import models

from website import settings


class Proposal(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=100)

    def __str__(self):
        return "title: " + str(self.title)
