from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    status = models.BooleanField(default=False)


class Comment(models.Model):
    body = models.TextField()
    sl = models.ForeignKey(Task, on_delete=models.CASCADE)
