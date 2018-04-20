from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from markdownx.models import MarkdownxField

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

class Raum(models.Model):
    bezeichnung = models.CharField(max_length=5)
    beschreibung = models.TextField(max_length=1000, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Räume'
    def __str__(self):
        return self.bezeichnung

class Belegung(models.Model):
    MY_CHOICES = (
        ('mo', 'Montag'),
        ('di', 'Dienstag'),
        ('mi', 'Mittwoch'),
        ('do', 'Donnerstag'),
        ('fr', 'Freitag'),
    )
    raum = models.ForeignKey(Raum, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=MY_CHOICES)
    course = models.ForeignKey(Kurs, on_delete=models.CASCADE, null=True, blank=True)
    beginn = models.TimeField()
    ende = models.TimeField()
    class Meta:
        verbose_name_plural = 'Belegungen'
    def __str__(self):
        return 'Belegung'

class Thema(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    erstellt = models.DateTimeField(default=timezone.now, editable=False)
    class Meta:
        verbose_name_plural = 'Neuigkeiten'
        verbose_name = 'Thema'
    def __str__(self):
        return self.title

class LehrerStundenplan(models.Model):
    name = models.CharField(max_length=200, default='Stundenplan')
    lehrer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': u'Lehrer'})
    class Meta:
        verbose_name_plural = 'Lehrer-Stundenpläne'
    def __str__(self):
        return self.name

class LehrerZeile(models.Model):
    beginn = models.TimeField(blank=True, null=True)
    ende = models.TimeField(blank=True, null=True)
    mo = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='lmo', null=True, blank=True)
    moraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='lmoraum', null=True, blank=True)
    di = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='ldi', null=True, blank=True)
    diraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='ldiraum', null=True, blank=True)
    mi = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='lmi', null=True, blank=True)
    miraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='lmiraum', null=True, blank=True)
    do = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='ldo', null=True, blank=True)
    doraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='ldoraum', null=True, blank=True)
    fr = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='lfr', null=True, blank=True)
    frraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='lfrraum', null=True, blank=True)
    s = models.ForeignKey(LehrerStundenplan, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Lehrer-Zeilen'
    def __str__(self):
        return str(self.beginn) + ' - ' + str(self.ende)

class LehrerFeld(models.Model):
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    raum = models.IntegerField()
    z = models.ForeignKey(LehrerZeile, on_delete=models.CASCADE, related_name='lz')
    class Meta:
        verbose_name_plural = 'Lehrer-Felder'
    def __str__(self):
        return self.kurs

class Stundenplan(models.Model):
    name = models.CharField(max_length=200, default='Stundenplan')
    klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Stundenpläne'
    def __str__(self):
        return self.name

class Zeile(models.Model):
    beginn = models.TimeField(blank=True, null=True)
    ende = models.TimeField(blank=True, null=True)
    mo = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='mo', null=True, blank=True)
    molehrer = models.ForeignKey(User, limit_choices_to={'groups__name': u'Lehrer'}, on_delete=models.CASCADE, related_name='mol', null=True, blank=True)
    moraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='moraum', null=True, blank=True)
    di = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='di', null=True, blank=True)
    dilehrer = models.ForeignKey(User, limit_choices_to={'groups__name': u'Lehrer'}, on_delete=models.CASCADE, related_name='dil', null=True, blank=True)
    diraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='diraum', null=True, blank=True)
    mi = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='mi', null=True, blank=True)
    milehrer = models.ForeignKey(User, limit_choices_to={'groups__name': u'Lehrer'}, on_delete=models.CASCADE, related_name='mil', null=True, blank=True)
    miraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='miraum', null=True, blank=True)
    do = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='do', null=True, blank=True)
    dolehrer = models.ForeignKey(User, limit_choices_to={'groups__name': u'Lehrer'}, on_delete=models.CASCADE, related_name='dol', null=True, blank=True)
    doraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='doraum', null=True, blank=True)
    fr = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='fr', null=True, blank=True)
    frlehrer = models.ForeignKey(User, limit_choices_to={'groups__name': u'Lehrer'}, on_delete=models.CASCADE, related_name='frl', null=True, blank=True)
    frraum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='frraum', null=True, blank=True)
    s = models.ForeignKey(Stundenplan, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Zeilen'
    def __str__(self):
        if self.beginn and self.ende:
            r = str(self.beginn) + ' - ' + str(self.ende)
        else:
            r = 'Keine Angabe'
        return r

class Feld(models.Model):
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='kurs')
    raum = models.ForeignKey(Raum, on_delete=models.CASCADE, related_name='raum')
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
