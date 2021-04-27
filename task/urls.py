from django.urls import path

from task.views import TaskViewSet, DoneListView, \
    CommentsListView, TaskMakeDone, MyTask, AddComment, CommentViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


main_router = DefaultRouter()
main_router.register(r'tasks', TaskViewSet, basename='task')
task_router = NestedDefaultRouter(main_router,'tasks', lookup='task')
task_router.register(r'comments', CommentViewSet, basename='task-comment')

urlpatterns = [
    *main_router.urls,
    *task_router.urls,
    path('done/', DoneListView.as_view(), name='done_list'),
    path('comments/<int:pk>/', CommentsListView.as_view(), name='comments_item'),
    path('makedone/<int:pk>/', TaskMakeDone.as_view(), name='taskdone__item'),
    path('mytask/<int:pk>/', MyTask.as_view(), name='mytask_item'),
    path('addcomment/', AddComment.as_view(), name='addcomment_item'),
]

