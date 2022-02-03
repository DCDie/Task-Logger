from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.EmailField(required=True)

    def to_internal_value(self, data):
        data["email"] = data["username"]
        return super().to_internal_value(data)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class ListUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(obj: User):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'username']
