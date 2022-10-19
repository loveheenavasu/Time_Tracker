from django import forms
from django.forms import ModelForm

from .models import Departments

class DepartmentsForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Departments
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'Project Name'}),
            'description': forms.Textarea(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-select',
                       'placeholder':'Project Description'})

        }