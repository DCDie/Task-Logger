from rest_framework import serializers
from apps.task.models import Task, Comment, TaskTimer
from apps.users.serializers import ListUserSerializer


class TaskListSerializer(serializers.ModelSerializer):
    worker = ListUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    total_time = serializers.DurationField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class AssignTaskSerializer(serializers.ModelSerializer):
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
