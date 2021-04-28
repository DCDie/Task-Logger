from django.contrib.auth.models import User
from rest_framework import serializers

from task.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AsignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['worker']


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
            'task': {'read_only': True}
        }
