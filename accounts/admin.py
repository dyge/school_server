from django.contrib import admin
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms

# class FachInline(admin.TabularInline):
#     model = models.Fach
#     extra = 5
#
# class KlassenAdmin(admin.ModelAdmin):
#     inlines = [FachInline]

class GerInline(admin.TabularInline):
    model = models.Ger
    extra = 1

class EngAdmin(admin.ModelAdmin):
    inlines = [GerInline]

class UserChangeFormExtended(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(UserChangeFormExtended, self).__init__(*args, **kargs)
        self.fields['klasse'] = forms.ModelChoiceField(label="Klasse", queryset=models.Klassen.objects.all())

class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['klasse'] = forms.ModelChoiceField(label="Klasse", queryset=models.Klassen.objects.all())

UserAdmin.form = UserChangeFormExtended

UserAdmin.fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'password', 'email', 'klasse', 'groups', 'is_staff')
    }),
)

UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username','email', 'password1', 'password2', 'klasse', 'groups', 'is_staff')
    }),
)

admin.site.register(models.Engvoc, EngAdmin)
admin.site.register(models.Klassen) #, KlassenAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
