from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from task.models import Task, Comment
from task.serializers import TaskSerializer, CommentSerializer, AsignSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title']

    @action(methods=['patch'], detail=True, url_path='assign', serializer_class=AsignSerializer)
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(methods=['get'], detail=True, url_path='get_comments', serializer_class=CommentSerializer)
    def comment_get(self, request, pk):
        com = Comment.objects.filter(taskid=pk)

        return Response(CommentSerializer(com, many=True).data)

    @action(methods=['post'], detail=True, url_path='add_comment', serializer_class=CommentSerializer)
    def task_assign(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance: Task = self.get_object()
        instance.body = serializer.validated_data['body']
        instance.save()

        response_serializer = TaskSerializer(instance)
        return Response(response_serializer.data)


class DoneListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        blogs = Task.objects.filter(status='True')

        return Response(TaskSerializer(blogs, many=True).data)


class CommentsListView(GenericAPIView):
    serializer_class = CommentSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        com = Comment.objects.filter(taskid=pk)

        return Response(CommentSerializer(com, many=True).data)


class TaskMakeDone(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.status = True
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class MyTask(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        author = Task.objects.filter(worker=pk)
        return Response(TaskSerializer(author, many=True).data)


class AddComment(GenericAPIView):
    serializer_class = CommentSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = Comment.objects.create(
            **serializer.validated_data,
        )
        comment.save()

        return Response(CommentSerializer(comment).data)
