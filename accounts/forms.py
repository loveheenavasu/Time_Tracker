
from django import forms
from .models import User


# create a ModelForm
class USerForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        fields = "__all__"