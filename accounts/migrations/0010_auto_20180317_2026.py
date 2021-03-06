# Generated by Django 2.0.3 on 2018-03-17 19:26

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_thema'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thema',
            options={'verbose_name_plural': 'Neuigkeiten'},
        ),
        migrations.AlterField(
            model_name='kurs',
            name='bezeichnung',
            field=models.CharField(default=3, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='thema',
            name='text',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
