# Generated by Django 2.0.3 on 2018-03-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20180317_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thema',
            name='text',
            field=models.TextField(),
        ),
    ]
