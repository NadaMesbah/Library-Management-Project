# Generated by Django 5.0.3 on 2024-05-17 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adherants', '0004_reclamation_useremail'),
        ('ouvrages', '0016_emprunt_automatique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date_demande',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adherants.profile'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='selected_copy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ouvrages.exemplaire'),
        ),
    ]