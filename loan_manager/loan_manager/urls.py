# Django imports
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

# Account app imports
from account.api import viewsets as account_viewsets

route = routers.DefaultRouter()
route.register(r'accounts', account_viewsets.AccountViewSet)

urlpatterns = [
    # User authentication
    path('admin/',
         admin.site.urls),
    path('login/',
         obtain_auth_token, name='login'),

    # Apps urls
    path('',
         include('transactions.urls')),
    path('account/',
         include(route.urls))
]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
