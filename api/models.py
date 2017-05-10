from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User

from website import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic_url = models.CharField(max_length=200)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Proposal(models.Model):
    user = models.ForeignKey('Profile', default=1, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', default=None, on_delete=models.CASCADE, blank=True, null=True)
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
