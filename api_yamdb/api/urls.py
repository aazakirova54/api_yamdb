from django.urls import include, path
from rest_framework import routers

from .views import (get_token, signup, UserViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='auth_signup'),
    path('v1/auth/token/', get_token, name='auth_token')
]
