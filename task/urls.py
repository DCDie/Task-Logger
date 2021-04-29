from task.views import TaskViewSet, CommentViewSet#, TimerViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


main_router = DefaultRouter()
main_router.register(r'tasks', TaskViewSet, basename='task')
task_router = NestedDefaultRouter(main_router, 'tasks', lookup='task')
task_router.register(r'comments', CommentViewSet, basename='task-comment')
#task_router.register(r'timers', TimerViewSet, basename='task-timer')

urlpatterns = [
    *main_router.urls,
    *task_router.urls,
]