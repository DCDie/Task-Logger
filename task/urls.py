from django.urls import path

from task.views import TaskViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
urlpatterns = router.urls

