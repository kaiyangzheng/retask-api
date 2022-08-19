from django.urls import path 
from .views import UserFriendRequest

urlpatterns = [
    path('friend/request/', UserFriendRequest.as_view(), name='friend-request'),
]