# Generated by Django 2.0.3 on 2018-04-10 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20180322_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='zeile',
            name='di',
            field=models.CharField(default=3, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zeile',
            name='do',
            field=models.CharField(default=3, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zeile',
            name='fr',
            field=models.CharField(default=3, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zeile',
            name='mi',
            field=models.CharField(default=3, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zeile',
            name='mo',
            field=models.CharField(default=3, max_length=50),
            preserve_default=False,
        ),
    ]
