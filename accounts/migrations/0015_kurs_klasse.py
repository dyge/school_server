# Generated by Django 2.0.3 on 2018-03-19 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_klassen_stellvertreter'),
    ]

    operations = [
        migrations.AddField(
            model_name='kurs',
            name='klasse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Klassen'),
        ),
    ]