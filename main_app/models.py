
from django.db import models
from django.conf import settings
from departments.models import Departments
# Create your models here.
PROJECT_CATEGORY = (
           ("UI/UX Design", "UI/UX Design"),
           ("Website Design", "Website Design"),
           ("App Development", "App Development"),
           ("Quality Assurance", "Quality Assurance"),
           ("Development", "Development"),
           ("Backend Development", "Backend Development"),
           ("Software Testing", "Software Testing"),
           ("Marketing", "Marketing"),
           ("SEO", "SEO"),
           ("Other", "Other"),
)
PRIORITY = (
    ('HIGHEST', 'Highest'),
    ('LOWEST', 'Lowest'),
    ('MEDIUM', 'Medium'),
)




class Projects(models.Model):
    project_name = models.CharField(max_length=255, null=True, blank=True)
    project_category = models.CharField(max_length=255, choices = PROJECT_CATEGORY, default = 'Other')
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name="assigned_to_user")
    is_ongoing = models.BooleanField(default=True)
    description = models.TextField(max_length=255)
    is_started = models.BooleanField(default=False)
    is_approval = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY, default='Lowest')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    task_category = models.CharField(max_length=255, choices=PROJECT_CATEGORY, default='Other')
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = 'users')
    task_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    in_progress = models.BooleanField(default=False)
    in_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=255, choices=PRIORITY, default='Lowest')
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


    





