from django.contrib import admin
from .models import Proposal, Category, Profile, ProposalVoteUser

admin.site.register(Proposal)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(ProposalVoteUser)
