from django.db import models
from django.utils import timezone


from django.contrib.auth.models import User

class Klassen(models.Model):
    bezeichnung = models.CharField(max_length=5)
    class Meta:
        verbose_name_plural = 'Klassen'
    def __str__(self):
        return self.bezeichnung

# klasse = models.ForeignKey(Klassen, on_delete=models.CASCADE)
# klasse.contribute_to_class(User, 'klasse')


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

#
# class Fach(models.Model):
#     title = models.CharField(max_length=200)
#     class Meta:
#         verbose_name_plural = 'Fächer'
#     def __str__(self):
#         return self.title
#
# class Schueler(models.Model):
#     fname = models.CharField(max_length=100)
#     lname = models.CharField(max_length=100)
#     klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE)
#     class Meta:
#         unique_together = ("fname", "lname")
#         verbose_name_plural = 'Schüler'
#     def get_absolute_url(self):
#         return reverse("home")
#     def __str__(self):
#         return self.fname + " " + self.lname
#
# class Lehrer(models.Model):
#     fname = models.CharField(max_length=100)
#     lname = models.CharField(max_length=100)
#     klassen = models.ManyToManyField(Klasse)
#     faecher = models.ManyToManyField(Fach)
#     class Meta:
#         unique_together = ("fname", "lname")
#         verbose_name_plural = 'Lehrer'
#     def get_absolute_url(self):
#         return reverse("home")
#     def __str__(self):
#         return self.fname + " " + self.lname
