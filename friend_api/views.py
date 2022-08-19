from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FriendRequestSerializer
from .models import FriendRequest
from authentication.models import CustomUser
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class UserFriendRequest(APIView):
    """
    Retrieve, create, or accept/reject friend request
    """
    permission_classes  = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    http_method_names = ['get', 'post', 'put']
    
    def get(self, request):
        # get all friend requests for current user
        friend_requests = FriendRequest.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'to_user': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def post(self, request):
        from_user = request.user
        to_user = CustomUser.objects.get(id=request.data['to_user'])
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return Response(status=status.HTTP_201_CREATED, data={'message': 'Friend request sent'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Friend request already sent'})
        
    def put(self, request):
        request_id = request.data['request_id']
        accept = request.data['accept']
        friend_request = FriendRequest.objects.get(id=request_id)
        if not friend_request:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Friend request not found'})
        
        if friend_request.to_user == request.user and accept:
            from_user = CustomUser.object.get(id=friend_request.from_user.id)
            to_user = CustomUser.object.get(id=friend_request.to_user.id)
            from_user.friends.add(to_user)
            to_user.friends.add(from_user)
            friend_request.delete()
            return Response(status=status.HTTP_200_OK, data={'message': 'Friend request accepted'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Friend request not accepted'})