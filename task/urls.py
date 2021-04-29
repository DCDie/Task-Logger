from task.views import TaskViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


main_router = DefaultRouter()
main_router.register(r'tasks', TaskViewSet, basename='task')
task_router = NestedDefaultRouter(main_router, 'tasks', lookup='task')
task_router.register(r'comments', CommentViewSet, basename='task-comment')

urlpatterns = [
    *main_router.urls,
    *task_router.urls,
]