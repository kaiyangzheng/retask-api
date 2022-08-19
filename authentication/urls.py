from django.urls import path 
from rest_framework_simplejwt import views as jwt_views
from .views import (
    CustomUserCreate,
    ObtainTokenPairView,
    UserList, 
    UserDetail, 
    UserDetailAdmin,
)

urlpatterns = [
    path('user/create/', CustomUserCreate.as_view(), name='user-create'),
    path('token/obtain/', ObtainTokenPairView.as_view(), name='token-obtain'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('user/', UserList.as_view(), name='user-list'),
    path('user/me', UserDetail.as_view(), name='user-detail'),
    path('admin/user/<int:user_id>/', UserDetailAdmin.as_view(), name='user-detail-admin'),
]