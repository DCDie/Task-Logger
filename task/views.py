from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from task.models import Task, Comment
from task.serializers import TaskSerializer, CommentSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class DoneListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        blogs = Task.objects.filter(status='True')

        return Response(TaskSerializer(blogs, many=True).data)


class TitleListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        tit = get_object_or_404(Task.objects.filter(title=pk))

        return Response(TaskSerializer(tit).data)


class CommentsListView(GenericAPIView):
    serializer_class = CommentSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        com = Comment.objects.filter(sl=pk)

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
