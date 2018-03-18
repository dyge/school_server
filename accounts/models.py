from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from markdownx.models import MarkdownxField

class Thema(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    erstellt = models.DateTimeField(default=timezone.now, editable=False)
    class Meta:
        verbose_name_plural = 'Neuigkeiten'
    def __str__(self):
        return self.title

class Klassen(models.Model):
    bezeichnung = models.CharField(max_length=5)
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
    stellvertreter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'}, related_name='Mystellvertreter')
    class Meta:
        verbose_name_plural = 'Klassen'
    def __str__(self):
        return self.bezeichnung

klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE, blank=True, null=True)
klasse.contribute_to_class(User, 'klasse')

def create_profile(sender,instance, *args, **kwargs):
    if not instance.password:
        instance.password = make_password('qwertzuiop')

pre_save.connect(create_profile, sender=User)

class Fach(models.Model):
    title = models.CharField(max_length=300)
    class Meta:
        verbose_name_plural = 'Fächer'
    def __str__(self):
        return self.title

class Kurs(models.Model):
    bezeichnung = models.CharField(max_length=500)
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
    stellvertreter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'}, blank=True, null=True, related_name='Stellvertreter')
    teilnehmer = models.ManyToManyField(User, related_name='Teilnehmer', blank=True)
    class Meta:
        verbose_name_plural = 'Kurse'
    def __str__(self):
        return self.bezeichnung

class Engvoc(models.Model):
    eng = models.CharField(max_length=200)
    ndatum = models.DateField(blank=True)
    def __str__(self):
        return self.eng
    class Meta:
        verbose_name_plural = "Englisch-Vokabeln"
    def save(self, *args, **kwargs):
        if not self.ndatum: # remove this line for real usage
            self.ndatum = timezone.now().date() # watch indentation
        return super(Engvoc, self).save(*args, **kwargs)

class Ger(models.Model):
    en = models.ForeignKey(Engvoc, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text
