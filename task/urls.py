from django.urls import path

from task.views import TaskViewSet, DoneListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls

urlpatterns += [
    path('task/done', DoneListView.as_view(), name='done_list'),
]

