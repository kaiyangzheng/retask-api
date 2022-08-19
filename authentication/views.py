from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, MyTokenObtainPairSerializer
from .models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password

# Create your views here.

class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer
    http_method_names = ['post']
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        })
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class CustomUserCreate(APIView):
    """
    Create a new user
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def post(self, request):
        serializer = CustomUserSerializer(data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': make_password(request.data.get('password')),
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserList(APIView):
    """
    List all users or create a new user
    """
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format='json'):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class UserDetail(APIView):
    """
    Retrieve, update, or delete user instance
    """
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, format='json'):
        user = CustomUser.objects.get(id=request.user.id)
        if not user:
            return Response(
                {'message': 'User with id {} does not exist'.format(request.user.id)},
            )
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def put(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        if not user:
            return Response(
                {'message': 'User with id {} does not exist'.format(request.user.id)},
            )
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        if not user:
            return Response(
                {'message': 'User with id {} does not exist'.format(request.user.id)},
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserDetailAdmin(APIView):
    """
    Retrieve, update, or delete user instance by admin
    """
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request, user_id, format='json'):
        user = CustomUser.objects.get(id=user_id)
        if not user:
            return Response(
                {'message': 'User with id {} does not exist'.format(user_id)},
            )
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        })
    )
    def put(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        if not user:
            return Response(
                {'message': 'User with id {} does not exist'.format(user_id)},
            )
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        if not user:
            return Response(
                {'message': 'User with id {} does not exist'.format(user_id)},
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    