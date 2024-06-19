# Generated by Django 5.0.6 on 2024-06-19 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LifeBetterApp', '0003_remove_visitante_estacionamiento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrovisitantedepto',
            name='rut_residente',
        ),
        migrations.AlterField(
            model_name='registrovisitantedepto',
            name='rut_visitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.visitante'),
        ),
    ]