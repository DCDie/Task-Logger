from django.urls import path

from task.views import TaskViewSet, DoneListView, TitleListView, CommentsListView, TaskMakeDone
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls

urlpatterns += [
    path('task/done', DoneListView.as_view(), name='done_list'),
    path('task/title/<slug:pk>/', TitleListView.as_view(), name='task_item'),
    path('task/comments/<int:pk>/', CommentsListView.as_view(), name='comments_item'),
    path('task/makedone/<int:pk>/', TaskMakeDone.as_view(), name='taskdone__item'),
]

