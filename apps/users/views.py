from django.db.models import Sum, OuterRef
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User

from apps.users.serializers import UserSerializer, ListUserSerializer
from apps.task.serializers import TaskSerializer, TimerSerializer
from apps.task.models import Task, TaskTimer


class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop('password', None)
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(UserSerializer(user).data)


class UserList(viewsets.ModelViewSet):
    serializer_class = ListUserSerializer
    queryset = User.objects.all()

    @action(methods=['get'], detail=False, url_path='month_time', serializer_class=TimerSerializer)
    def month_time(self, request):
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = timezone.now()
        prev_month = TaskTimer.objects.filter(stop_time__range=[start_date, end_date],
                                              author=self.request.user).aggregate(Sum('time_final'))
        sum_time = prev_month['time_final__sum'] / 60

        return Response(sum_time)

    @action(methods=['get'], detail=False, url_path='top', serializer_class=TaskSerializer)
    def top(self, request):
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = timezone.now()
        subquery = TaskTimer.objects.filter(task=OuterRef('id'), stop_time__range=[start_date, end_date]).values(
            'task').annotate(total_time=Sum('time_final')).values('total_time')
        queryset = Task.objects.annotate(total_time=subquery).order_by('-total_time')[:20]

        return Response(TaskSerializer(queryset, many=True).data)
