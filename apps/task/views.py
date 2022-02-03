import random
import uuid
from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
from rest_framework_nested.viewsets import NestedViewSetMixin
from django.utils import timezone
from django.db.models import Sum

from apps.task.models import Task, Comment, TaskTimer
from apps.task.serializers import (
    TaskSerializer, CommentSerializer, AssignTaskSerializer, TaskStatusSerializer, TimerSerializer, TimerAddSerializer,
    TaskListSerializer)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related('worker')
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'body']
    filter_fields = ['done', 'worker']

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return self.serializer_class

    @action(methods=['patch'], detail=True, url_path='assign', serializer_class=AssignTaskSerializer)
    def task_assign(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        instance.worker.email_user(subject=instance.title,
                                   message=instance.body,
                                   from_email='danielcuznetov04@gmail.com',
                                   fail_silently=False, )
        return Response(TaskSerializer(instance).data)

    @action(methods=['patch'], detail=True, url_path='complete', serializer_class=TaskStatusSerializer)
    def task_complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.done = True
        instance.done_date = timezone.now()
        instance.save()

        user_ids = instance.comment_set.values_list('author', flat=True).distinct()
        users = User.objects.filter(id__in=user_ids)
        for user in users:
            user.email_user(subject='Task that you commented was completed!',
                            message=instance.name,
                            from_email='danielcuznetov04@gmail.com',
                            fail_silently=False, )

        return Response(TaskSerializer(instance).data)

    @action(methods=['get'], detail=False, url_path='done_tasks', serializer_class=TaskSerializer)
    def get_done_tasks(self, request):
        tasks = Task.objects.filter(done='True')
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['get'], detail=False, url_path='my_tasks', serializer_class=TaskSerializer)
    def get_my_tasks(self, request):
        tasks = Task.objects.filter(worker=self.request.user)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['post'], detail=False, url_path='add_25000_tasks', serializer_class=TaskSerializer)
    def crate_tasks(self, request):
        i: int = 1
        mylist = [False, True]
        for i in range(25000):
            new_task = Task.objects.create(
                title=uuid.uuid4(),
                body=uuid.uuid4(),
                done=random.choice(mylist),
                worker_id=User.objects.filter().order_by('?').first().id,
            )
            new_task.save()

        return Response("Task done!")

    @action(methods=['post'], detail=False, url_path='add_50000_logs', serializer_class=TimerSerializer)
    def crate_logs(self, request):
        i: int = 0
        for i in range(50000):
            new_log = TaskTimer.objects.create(
                task_id=Task.objects.filter().order_by('?').first().id,
                author_id=User.objects.filter().order_by('?').first().id,
                stop_time=timezone.now(),
                time_final=timedelta(seconds=random.randint(60, 3600)),

            )
            new_log.start_time = new_log.stop_time - new_log.time_final
            new_log.save()

        return Response("Task done!")


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
