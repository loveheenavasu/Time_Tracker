
from django import forms
from .models import User


# create a ModelForm
class UserForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        fields = ('fullname','is_employee', 'is_staff','image','country','is_active','is_TeamLeader','email', 'contact', 'education', 'experience', 'City', 'password', 'description', 'department', 'address', 'designation', 'is_admin', 'date_joined','is_projectmanager', 'username')
        widgets = {
            'fullname': forms.TextInput(attrs={'type': 'text', 'for': "exampleFormControlInput877" , 'class': 'form-control', 'placeholder': 'Employee Name'}),
            'password': forms.TextInput(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'password'}),
            'email': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Email'}),
            'contact': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Contact'}),
            'country': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Country'}),
            'education': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Education'}),
            'experience': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Working Experience'}),
            'City': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'City'}),
            'description': forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Description about the user'}),
            'department': forms.Select(attrs={'type': 'text', 'class': 'form-control'}),
            'address': forms.Textarea(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Current Address'}),
            'designation': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Designation'}),
            'username': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Username'}),

        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('fullname','is_employee', 'is_staff','image','is_active','is_TeamLeader','email', 'contact', 'education', 'experience', 'City', 'password', 'description', 'department', 'address', 'designation', 'is_admin', 'date_joined','is_projectmanager', 'username')
        widgets = {
            'fullname': forms.TextInput(attrs={'type': 'text', 'for': "exampleFormControlInput877" , 'class': 'form-control', 'placeholder': 'Employee Name'}),
            'password': forms.TextInput(
                attrs={'type': 'text', 'for': "exampleFormControlInput877", 'class': 'form-control',
                       'placeholder': 'password'}),
            'education': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Email'}),
            'contact': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Contact'}),
            'experience': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Working Experience'}),
            'City': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'City'}),
            'description': forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Description about the user'}),
            'department': forms.Select(attrs={'type': 'text', 'class': 'form-control'}),
            'address': forms.Textarea(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Current Address'}),
            'designation': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Designation'}),
            'username': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Username'}),

        }