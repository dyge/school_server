# Generated by Django 2.0.3 on 2018-04-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_auto_20180413_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='raum',
            name='beschreibung',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]