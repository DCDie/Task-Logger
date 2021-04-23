from django.urls import path

from users.views import RegisterUserView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token_register'),
]
