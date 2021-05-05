from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.contrib import django_filters
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from rest_framework_nested.viewsets import NestedViewSetMixin
from django.utils import timezone
from django.db.models import Sum

from task.filtersets import TaskTimerFilterSet
from task.models import Task, Comment, TaskTimer
from task.serializers import TaskSerializer, CommentSerializer, AsignTaskSerializer, TaskStatusSerializer, \
    TimerSerializer, TimerAddSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['patch'], detail=True, url_path='assign', serializer_class=AsignTaskSerializer)
    def task_assign(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance: Task = self.get_object()
        instance.worker = serializer.validated_data['worker']
        instance.save()

        instance.worker.email_user('You have a new task!',
                                   'Complite the task!',
                                   'danielcuznetov04@gmail.com',
                                   fail_silently=False, )

        response_serializer = TaskSerializer(instance)
        return Response(response_serializer.data)

    @action(methods=['patch'], detail=True, url_path='complete', serializer_class=TaskStatusSerializer)
    def task_complete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance: Task = self.get_object()
        instance.status = serializer.validated_data['status']
        instance.save()

        user_ids = instance.comment_set.values_list('author', flat=True).distinct()
        users = User.objects.filter(id__in=user_ids)

        for user in users:
            user.email_user('Task that you commented was completed!',
                            'Task was completed!',
                            'danielcuznetov04@gmail.com',
                            fail_silently=False, )

        response_serializer = TaskSerializer(instance)
        return Response(response_serializer.data)

    @action(methods=['get'], detail=False, url_path='done_tasks', serializer_class=TaskSerializer)
    def get_done_tasks(self, request):
        done = Task.objects.filter(status='True')

        return Response(TaskSerializer(done, many=True).data)

    @action(methods=['get'], detail=False, url_path='my_tasks', serializer_class=TaskSerializer)
    def get_my_tasks(self, request):
        author = self.request.user
        my_task = Task.objects.filter(worker=author)

        return Response(TaskSerializer(my_task, many=True).data)


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    parent_lookup_kwargs = {
        'task_pk': 'task__pk'
    }

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_pk'))
        author = self.request.user
        serializer.save(task=task, author=author)

    def create(self, request, *args, **kwargs):
        serializer: CommentSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        serializer.instance.task.worker.email_user('Your task has been commented',
                                                   'Read the comment!',
                                                   'danielcuznetov04@gmail.com',
                                                   fail_silently=False, )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TaskTimerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TimerSerializer
    queryset = TaskTimer.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = TaskTimerFilterSet
    permission_classes = [IsAuthenticated]
    parent_lookup_kwargs = {
        'task_pk': 'task__pk'
    }

    @action(methods=['post'], detail=False, url_path='start_timer', serializer_class=TimerSerializer)
    def start_timer(self, request, task_pk):
        instance = TaskTimer.objects.create(
            task_id=task_pk,
            author=self.request.user,
            start_time=timezone.now(),
        )

        return Response(TimerSerializer(instance).data)

    @action(methods=['post'], detail=False, url_path='stop_timer', serializer_class=TimerSerializer)
    def stop_timer(self, request, task_pk):
        instance = get_object_or_404(TaskTimer, author=self.request.user, task=task_pk, stop_time__isnull=True)
        instance.stop_time = timezone.now()
        instance.time_final = (instance.stop_time - instance.start_time)
        instance.save()

        return Response(TimerSerializer(instance).data)

    @action(methods=['post'], detail=False, url_path='log_time', serializer_class=TimerAddSerializer)
    def log_timer(self, request, task_pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = TaskTimer.objects.create(
            task_id=task_pk,
            author=self.request.user,
            stop_time=serializer.validated_data['stop_time'],
            time_final=serializer.validated_data['time_final'] * 60,
        )

        instance.start_time = instance.stop_time - instance.time_final
        instance.save()

        return Response(TimerAddSerializer(instance).data)

    @action(methods=['get'], detail=False, url_path='tasks_logs', serializer_class=TimerSerializer)
    def tasks_logs(self, request, task_pk):
        queryset = self.filter_queryset(TaskTimer.objects.filter(task=task_pk))
        return Response(TimerSerializer(queryset, many=True).data)

    @action(methods=['get'], detail=False, url_path='sum_time', serializer_class=TimerSerializer)
    def sum_time(self, request, task_pk):
        sum_time = TaskTimer.objects.filter(task=task_pk).aggregate(Sum('time_final'))
        suma = sum_time['time_final__sum'] / 60
        return Response(suma)

