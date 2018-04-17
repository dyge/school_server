from django.contrib import admin
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django_summernote.admin import SummernoteModelAdmin
import nested_admin

class FelderInline(nested_admin.NestedStackedInline):
    model = models.Feld
    extra = 5

class ZeilenInline(nested_admin.NestedStackedInline):
    model = models.Zeile
    inlines = [FelderInline, ]
    extra = 8

class StundenplanAdmin(nested_admin.NestedModelAdmin):
    inlines = [ZeilenInline, ]

class LehrerFelderInline(nested_admin.NestedStackedInline):
    model = models.LehrerFeld
    extra = 5

class LehrerZeilenInline(nested_admin.NestedStackedInline):
    model = models.LehrerZeile
    inlines = [LehrerFelderInline, ]
    extra = 8

class LehrerStundenplanAdmin(nested_admin.NestedModelAdmin):
    inlines = [LehrerZeilenInline, ]

class KursAdmin(admin.ModelAdmin):
    filter_horizontal = ('teilnehmer',)

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

class ThemaAdmin(SummernoteModelAdmin):
    summernote_fields = ('text', )

admin.site.register(models.Engvoc, EngAdmin)
admin.site.register(models.Kurs, KursAdmin)
admin.site.register(models.Klassen)
admin.site.register(models.Fach)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Thema, ThemaAdmin)
admin.site.register(models.Stundenplan, StundenplanAdmin)
admin.site.register(models.LehrerStundenplan, LehrerStundenplanAdmin)
admin.site.register(models.Belegung)
admin.site.register(models.Raum)
