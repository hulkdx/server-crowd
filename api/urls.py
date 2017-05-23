from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    # /api/proposal
    url(r'^proposal$', views.ProposalListAPIView.as_view(), name='proposals'),
    # /api/proposal/<pk>/
    url(r'^proposal/(?P<pk>\d+)/$', views.ProposalDetailAPIView.as_view(), name='proposal'),
    # /api/proposal/create
    url(r'^proposal/create$', views.ProposalCreate.as_view(), name='proposals'),
    # /api/proposal/vote
    url(r'^proposal/(?P<pk>\d+)/vote$', views.ProposalVoteUpdate.as_view(), name='proposals'),

    # /api/register
    url(r'^register$', views.UserCreate.as_view(), name='register'),
    # /api/login
    url(r'^login', views.UserLogin.as_view(), name='login'),

    # /api/category
    url(r'^category$', views.CategoryListAPIView.as_view(), name='proposals'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
