# Generated by Django 5.0.6 on 2024-06-15 03:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LifeBetterApp', '0002_rename_run_residente_registrovisitantedepto_rut_residente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id_depto', models.AutoField(primary_key=True, serialize=False)),
                ('numero_depto', models.IntegerField()),
                ('piso', models.IntegerField()),
            ],
            options={
                'db_table': 'departamento',
            },
        ),
        migrations.AlterField(
            model_name='adminempleadocontratada',
            name='id_admin_empleado_contratada',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='id_asunto',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bitacora',
            name='id_bitacora',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='encomienda',
            name='id_encomienda',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='espaciocomun',
            name='id_ec',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='id_estacionamiento',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='multa',
            name='id_multa',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registrovisitantedepto',
            name='id_visitante_depto',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reservacion',
            name='id_reservacion',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('adminedificio', 'Administrador'), ('conserje', 'Conserje'), ('residente', 'Residente')], default='adminedificio', max_length=100),
        ),
        migrations.AddField(
            model_name='encomienda',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AddField(
            model_name='estacionamiento',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AddField(
            model_name='multa',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AddField(
            model_name='registrovisitantedepto',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AddField(
            model_name='reservacion',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AddField(
            model_name='residente',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AddField(
            model_name='visitante',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id_reclamo', models.AutoField(primary_key=True, serialize=False)),
                ('asunto', models.CharField(max_length=60)),
                ('contenido_reclamo', models.CharField(max_length=200)),
                ('fecha_hora_reclamo', models.DateTimeField()),
                ('departamento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento')),
                ('run_residente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.residente')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id_respuesta', models.AutoField(primary_key=True, serialize=False)),
                ('contenido_respuesta', models.CharField(max_length=200)),
                ('fecha_hora_respuesta', models.DateTimeField()),
                ('id_reclamo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.reclamo')),
                ('run_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.empleado')),
            ],
        ),
    ]