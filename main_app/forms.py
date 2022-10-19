from django import forms
from django.forms import ModelForm

from .models import Projects, Task


# create a ModelForm
class ProjectsForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Projects
        fields = ('project_name', 'status','priority','project_category', 'is_ongoing', 'description', 'department', 'is_completed', 'completed_at','deadline')
        widgets = {
            'project_name': forms.TextInput(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),

            'project_category': forms.Select(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),
            'department': forms.Select(attrs={'type': 'text', 'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-select',
                       'placeholder':'Project Description'}),
            'status': forms.Select(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),
            'priority': forms.Select(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),



        }


class UpdateProjectForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Projects
        # fields = '__all__'
        fields = ('project_name', 'status', 'priority', 'project_category', 'is_ongoing', 'description', 'department',
                  'is_completed', 'completed_at', 'deadline')
        widgets = {
            'project_name': forms.TextInput(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),

            'project_category': forms.Select(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),
            'department': forms.Select(attrs={'type': 'text', 'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-select',
                       'placeholder': 'Project Description'}),
            'status': forms.Select(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),
            'priority': forms.Select(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),
        }

class TaskForm(ModelForm):
  class Meta:
    model = Task
    fields = ('priority', 'project', 'task_category' ,'assigned_to', 'task_name', 'description', 'in_progress', 'in_review', 'is_completed', 'deadline')
    widgets ={
        'task_name': forms.TextInput(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                   'placeholder': 'Project Name'}),
        'project': forms.Select(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control'}),
        'task_category': forms.Select(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control'}),
        'assigned_to': forms.SelectMultiple(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control'}),
        'priority': forms.Select(attrs={'type': 'text', 'class': 'form-control'}),
        'description': forms.Textarea(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-select',
                   'placeholder': 'Project Description'}),
    }

class UpdateTaskForm(ModelForm):
  class Meta:
    model = Task
    fields = ('priority', 'project', 'task_category' ,'assigned_to', 'task_name', 'description', 'in_progress', 'in_review', 'is_completed', 'deadline')
    widgets ={
        'task_name': forms.TextInput(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                   'placeholder': 'Project Name'}),
        'project': forms.Select(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control'}),
        'task_category': forms.Select(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control'}),
        'assigned_to': forms.SelectMultiple(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control'}),
        'priority': forms.Select(attrs={'type': 'text', 'class': 'form-control'}),
        'description': forms.Textarea(
            attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-select',
                   'placeholder': 'Project Description'}),
    }
