from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save

class Klassen(models.Model):
    bezeichnung = models.CharField(max_length=5)
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
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
    # klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE)
    # fach = models.ForeignKey(Fach, on_delete=models.CASCADE)
    bezeichnung = models.CharField(max_length=500, blank=True, null=True)
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
    teilnehmer = models.ManyToManyField(User, related_name='Teilnehmer')   # , on_delete=models.CASCADE, related_name='Nutzer'
    class Meta:
        verbose_name_plural = 'Kurse'
    def __str__(self):
        return self.bezeichnung

def create_kurs(sender,instance, *args, **kwargs):
    if not instance.bezeichnung:
        instance.bezeichnung = str(instance.fach) + ' ' + str(instance.klasse)

pre_save.connect(create_kurs, sender=Kurs)

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
