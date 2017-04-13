from django.conf.urls import include, url

from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/token/', obtain_jwt_token),
    url(r'^api/', include('api.urls')),

]
