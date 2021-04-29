from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework_nested.viewsets import NestedViewSetMixin
from datetime import datetime

from task.models import Task, Comment, TaskTimer
from task.serializers import TaskSerializer, CommentSerializer, AsignTaskSerializer, TaskStatusSerializer, \
    TimerSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    # def get_queryset(self):
    # return super(TaskViewSet, self).get_queryset().filter(worker=self.request.user)

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

    @action(methods=['get'], detail=True, url_path='start_timer', serializer_class=TimerSerializer)
    def start_timer(self, request, pk):
        instance = TaskTimer.objects.create(
            task_id=pk,
            author=self.request.user,
            start_time=timezone.now(),
        )

        return Response(TimerSerializer(instance).data)

    @action(methods=['get'], detail=True, url_path='stop_timer', serializer_class=TimerSerializer)
    def stop_timer(self, request, pk):
        instance = get_object_or_404(TaskTimer, author=self.request.user, task=pk, stop_time__isnull=True)
        instance.stop_time = timezone.now()
        instance.time_final = (instance.stop_time - instance.start_time)
        instance.save()

        return Response(TimerSerializer(instance).data)


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


"""class TimerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TimerSerializer
    queryset = TaskTimer.objects.all()
    permission_classes = [IsAuthenticated]
    parent_lookup_kwargs = {
        'task_pk': 'task__pk'
    }"""
