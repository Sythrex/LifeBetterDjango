# Generated by Django 5.0.6 on 2024-07-05 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LifeBetterApp', '0008_merge_20240705_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('adminedificio', 'Administrador'), ('conserje', 'Conserje')], default='adminedificio', max_length=13),
        ),
    ]
