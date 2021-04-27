# Create your views here.

from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.serializers import UserSerializer, AllUsers
from django.core.mail import send_mail


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.pop('password', None)
        user = User.objects.create(
            **serializer.validated_data,
        )
        user.set_password(password)
        user.username = user.email
        user.save()
        return Response(UserSerializer(user).data)


class UserList(viewsets.ModelViewSet):
    serializer_class = AllUsers
    queryset = User.objects.all()
