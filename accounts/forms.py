from django import forms
from . import models

class UserForm(forms.Form):
    username = forms.CharField(required=True,max_length=200)
    password = forms.CharField(required=True, max_length=200, widget = forms.PasswordInput())

class EngForm(forms.ModelForm):
    class Meta:
        fields = ['eng',]
        model = models.Engvoc
