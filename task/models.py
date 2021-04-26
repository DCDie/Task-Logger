from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    status = models.BooleanField(default=False)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Comment(models.Model):
    body = models.TextField()
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE)
