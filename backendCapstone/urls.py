from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from capstone.models import *
from capstone.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'player', Players, 'player')
router.register(r'user', Users, 'user')
router.register(r'category', Categories, 'category')
router.register(r'message', Messages, 'message')
router.register(r'event', Events, 'event')
router.register(r'game', Games, 'game')
router.register(r'playerevent', PlayerEvents, 'playerevent')




urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
