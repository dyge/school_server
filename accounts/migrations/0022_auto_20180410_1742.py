# Generated by Django 2.0.3 on 2018-04-10 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20180410_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zeile',
            name='di',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='di', to='accounts.Kurs'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='do',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='do', to='accounts.Kurs'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='fr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fr', to='accounts.Kurs'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='mi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mi', to='accounts.Kurs'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='mo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mo', to='accounts.Kurs'),
        ),
    ]