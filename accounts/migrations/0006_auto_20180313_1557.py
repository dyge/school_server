# Generated by Django 2.0.3 on 2018-03-13 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180313_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kurs',
            name='bezeichnung',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
