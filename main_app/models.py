from django.db import models
from django.conf import settings
# Create your models here.
class Projects(models.Model):
    project = models.CharField(max_length=255, null=True, blank=True)
    is_ongoing = models.BooleanField(default=True)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)


class Task(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    task_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)

class Remarks(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=255) 
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    submission = models.DateTimeField()


    





