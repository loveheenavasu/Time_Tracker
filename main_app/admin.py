from django.contrib import admin
from main_app.models import Task
from . models import Projects, Remarks,TaskAssignment
# Register your models here.
admin.site.register(Task)
admin.site.register(Projects)
admin.site.register(Remarks)
admin.site.register(TaskAssignment)
