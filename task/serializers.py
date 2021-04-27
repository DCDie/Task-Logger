from django.contrib.auth.models import User
from rest_framework import serializers

from task.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AsignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'worker']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body']
