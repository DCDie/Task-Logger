from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    status = models.BooleanField(default=False)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class TaskTimer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    stop_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    time_final = models.DurationField(null=True)

