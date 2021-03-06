# Generated by Django 2.0.3 on 2018-04-14 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_raum_beschreibung'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zeile',
            name='diraum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diraum', to='accounts.Raum'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='doraum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doraum', to='accounts.Raum'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='frraum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='frraum', to='accounts.Raum'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='miraum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='miraum', to='accounts.Raum'),
        ),
        migrations.AlterField(
            model_name='zeile',
            name='moraum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moraum', to='accounts.Raum'),
        ),
    ]
