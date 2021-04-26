# Create your views here.
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserSerializer


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
            user.save()

            return Response(UserSerializer(user).data)