from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    # /api/proposal
    url(r'^proposal$', views.ProposalListAPIView.as_view(), name='proposals'),
    # /api/proposal/<pk>/
    url(r'^proposal/(?P<pk>\d+)/$', views.ProposalDetailAPIView.as_view(), name='proposal'),

    # /api/register
    url(r'^register$', views.UserCreate.as_view(), name='register'),
    # /api/login
    url(r'^login', views.UserLogin.as_view(), name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
