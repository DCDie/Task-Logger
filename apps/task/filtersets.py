from django_filters import rest_framework as filters
from apps.task.models import TaskTimer


class TaskTimerFilterSet(filters.FilterSet):
    class Meta:
        model = TaskTimer
        fields = '__all__'
