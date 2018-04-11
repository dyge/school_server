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
        verbose_name = 'Thema'
    def __str__(self):
        return self.title

class Klassen(models.Model):
    bezeichnung = models.CharField(max_length=5)
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
    stellvertreter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'}, related_name='Mystellvertreter')
    class Meta:
        verbose_name_plural = 'Klassen'
        verbose_name = 'Klasse'
    def __str__(self):
        return self.bezeichnung

klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE, blank=True, null=True)
klasse.contribute_to_class(User, 'klasse')

class Kurs(models.Model):
    bezeichnung = models.CharField(max_length=500)
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
    stellvertreter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'}, blank=True, null=True, related_name='Stellvertreter')
    klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE, blank=True, null=True)
    teilnehmer = models.ManyToManyField(User, related_name='Teilnehmer', blank=True)
    class Meta:
        verbose_name_plural = 'Kurse'
        verbose_name = 'Kurs'
    def __str__(self):
        return self.bezeichnung

class Stundenplan(models.Model):
    name = models.CharField(max_length=200, default='Stundenplan')
    klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Stundenpläne'
    def __str__(self):
        return self.name

class Zeile(models.Model):
    zeit = models.CharField(max_length=5)
    mo = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='mo', null=True, blank=True)
    di = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='di', null=True, blank=True)
    mi = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='mi', null=True, blank=True)
    do = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='do', null=True, blank=True)
    fr = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='fr', null=True, blank=True)
    s = models.ForeignKey(Stundenplan, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Zeilen'
    def __str__(self):
        return self.zeit

class Feld(models.Model):
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    raum = models.IntegerField()
    z = models.ForeignKey(Zeile, on_delete=models.CASCADE, related_name='z')
    class Meta:
        verbose_name_plural = 'Felder'
    def __str__(self):
        return self.kurs

def create_profile(sender,instance, *args, **kwargs):
    if not instance.password:
        instance.password = make_password('qwertzuiop')

pre_save.connect(create_profile, sender=User)

class Fach(models.Model):
    title = models.CharField(max_length=300)
    class Meta:
        verbose_name_plural = 'Fächer'
        verbose_name = 'Fach'
    def __str__(self):
        return self.title

class Engvoc(models.Model):
    eng = models.CharField(max_length=200)
    ndatum = models.DateField(blank=True)
    def __str__(self):
        return self.eng
    class Meta:
        verbose_name_plural = "Englisch-Vokabeln"
        verbose_name = 'Englisch-Vokabel'
    def save(self, *args, **kwargs):
        if not self.ndatum: # remove this line for real usage
            self.ndatum = timezone.now().date() # watch indentation
        return super(Engvoc, self).save(*args, **kwargs)

class Ger(models.Model):
    en = models.ForeignKey(Engvoc, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text
