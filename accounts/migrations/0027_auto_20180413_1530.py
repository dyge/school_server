# Generated by Django 2.0.3 on 2018-04-13 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0026_lehrerfeld'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lehrerstundenplan',
            options={'verbose_name_plural': 'Lehrer-Stundenpläne'},
        ),
        migrations.AddField(
            model_name='lehrerstundenplan',
            name='lehrer',
            field=models.ForeignKey(default=5, limit_choices_to={'groups__name': 'Lehrer'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]