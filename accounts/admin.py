from django.contrib import admin
from . import models

class GerInline(admin.TabularInline):
    model = models.Ger
    extra = 1

class EngAdmin(admin.ModelAdmin):
    inlines = [GerInline]

admin.site.register(models.Engvoc, EngAdmin)
