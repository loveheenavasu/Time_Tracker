from enum import unique
from re import T
from django.db import models
from django.conf import settings
from departments.models import Departments
from django.conf.global_settings import AUTH_USER_MODEL
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
    ('Highest', 'Highest'),
    ('Lowest', 'Lowest'),
    ('Medium', 'Medium'),
)

STATUS = (
    ('Todo', 'Todo'),
    ('In Development', 'In Development'),
    ('Completed', 'Completed'),
    ('Approval', 'Approval'),
)



class Projects(models.Model):
    project_name = models.CharField(max_length=255, null=True, blank=True)
    project_category = models.CharField(max_length=255, choices=PROJECT_CATEGORY, default='Other')
    is_ongoing = models.BooleanField(default=True)
    description = models.TextField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS, null=True, blank=True)
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

    def get_all_task_users(self):
        task_lists = Task.objects.filter(project=self).all()
        all_assigned_users = []
        user_id =[]# print("Filtered tasks for specific project : ", task_lists)
        for task in task_lists:
            for user in task.assigned_to.all():
                all_assigned_users.append(user.image)
                user_id.append(user.id)
        return set(all_assigned_users)

    def get_all_task_users_number(self):
        task_lists = Task.objects.filter(project=self).all()
        all_assigned_users = []        # print("Filtered tasks for specific project : ", task_lists)
        for task in task_lists:
            for user in task.assigned_to.all():
                all_assigned_users.append(user.image)
        total_members = set(all_assigned_users)
        print("len(total_members) : ", len(total_members))
        return len(total_members)


class Task(models.Model):
    task_name = models.CharField(max_length=1000, null=True, blank=True)
    task_category = models.CharField(max_length=255, choices=PROJECT_CATEGORY, default='Other')
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='users')
    priority = models.CharField(max_length=255, choices=PRIORITY, default='Lowest')
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS, null=True, blank=True)
    in_progress = models.BooleanField(default=False)
    in_review = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    start_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    task_created_by = models.CharField(max_length=255, null=True, blank=True)


    def get_assigned_users(self):
        users_list = []
        # print("Self assigfned : ", self.task_name, " - ", self.assigned_to.all())
        task_users = self.assigned_to.all();
        print('all assigned users for : ', self.task_name, task_users)
        for user in task_users:
            users_list.append(user.image)
        return users_list

    # def get_assigned_task_users_usera(self):
    #     users_list = []
    #     # print("Self assigfned : ", self.task_name, " - ", self.assigned_to.all())
    #     task_users = self.assigned_to.filter(id=id);
    #     print(task_users,'------------------------------------------->')
    #     print('all assigned users for : ', self.task_name, task_users)
    #     for user in task_users:
    #         users_list.append(user.image)
    #     return users_list


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


