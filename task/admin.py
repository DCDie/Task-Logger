from django.contrib import admin
from task.models import Task, Comment, TaskTimer

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(TaskTimer)
