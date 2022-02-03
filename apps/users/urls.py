from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView, )

from apps.users.views import RegisterUserView, UserList

router = DefaultRouter()
router.register(r'users', UserList, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterUserView.as_view(), name='user_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
