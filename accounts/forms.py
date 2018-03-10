from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.Form):
    username = forms.CharField(required=True,max_length=200)
    password = forms.CharField(required=True, max_length=200, widget = forms.PasswordInput())

class EngForm(forms.ModelForm):
    class Meta:
        fields = ['eng',]
        model = models.Engvoc

class SchuelerForm(UserCreationForm):
    klasse = forms.ModelChoiceField(queryset=models.Klassen.objects.all())
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
    class Meta:
        fields = ['username', 'email', 'klasse', 'password1', 'password2']
        model = User
