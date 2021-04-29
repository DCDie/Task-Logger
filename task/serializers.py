from django.contrib.auth.models import User
from rest_framework import serializers

from task.models import Task, Comment, TaskTimer


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


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTimer
        fields = '__all__'


class TimerAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTimer
        fields = ['stop_time', 'time_final']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
            'task': {'read_only': True}
        }
