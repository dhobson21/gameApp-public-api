from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from capstone.models import *
from capstone.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'players', Players, 'player')
router.register(r'user', Users, 'user')
router.register(r'categories', Categories, 'category')
router.register(r'messages', Messages, 'message')
router.register(r'events', Events, 'event')
router.register(r'games', Games, 'game')
router.register(r'playerevents', PlayerEvents, 'playerevent')




urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
