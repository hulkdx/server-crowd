from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic_url = models.CharField(max_length=200)

    def __str__(self):
        return "user: " + str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Proposal(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', default=None, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField(default=timezone.now, blank=True, null=True)
    description = models.CharField(max_length=500)
    votedYes = models.IntegerField(default=0)
    votedNo = models.IntegerField(default=0)
    articles = models.IntegerField(default=0)
    discussions = models.IntegerField(default=0)
    # TODO: ATTACHMENT

    def __str__(self):
        return "title: " + str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=80, default="")
    source_fill = models.CharField(max_length=200, default="")
    source = models.CharField(max_length=200)

    def __str__(self):
        return "name: " + str(self.name)


class Discussion(models.Model):
    user = models.ForeignKey('Profile')
    proposal = models.ForeignKey('Proposal')
    comment = models.CharField(max_length=500, default='')
    upvoted = models.IntegerField(default=0)
    downvoted = models.IntegerField(default=0)
    isUpvoted = models.NullBooleanField(default=None)


class ProposalVoteUser(models.Model):
    user = models.ForeignKey('Profile')
    proposal = models.ForeignKey('Proposal')
    vote = models.BooleanField()
