# Generated by Django 5.0.6 on 2024-06-18 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LifeBetterApp', '0003_departamento_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminempleadocontratada',
            options={'verbose_name': 'Admin Empleado Contratada', 'verbose_name_plural': 'Admin Empleados Contratadas'},
        ),
        migrations.AlterModelOptions(
            name='administracionexterna',
            options={'verbose_name': 'Administración Externa', 'verbose_name_plural': 'Administraciones Externas'},
        ),
        migrations.AlterModelOptions(
            name='anuncio',
            options={'verbose_name': 'Anuncio', 'verbose_name_plural': 'Anuncios'},
        ),
        migrations.AlterModelOptions(
            name='bitacora',
            options={'verbose_name': 'Bitácora', 'verbose_name_plural': 'Bitácoras'},
        ),
        migrations.AlterModelOptions(
            name='departamento',
            options={'verbose_name': 'Departamento', 'verbose_name_plural': 'Departamentos'},
        ),
        migrations.AlterModelOptions(
            name='empleado',
            options={'verbose_name': 'Empleado', 'verbose_name_plural': 'Empleados'},
        ),
        migrations.AlterModelOptions(
            name='encomienda',
            options={'verbose_name': 'Encomienda', 'verbose_name_plural': 'Encomiendas'},
        ),
        migrations.AlterModelOptions(
            name='espaciocomun',
            options={'verbose_name': 'Espacio Común', 'verbose_name_plural': 'Espacios Comunes'},
        ),
        migrations.AlterModelOptions(
            name='estacionamiento',
            options={'verbose_name': 'Estacionamiento', 'verbose_name_plural': 'Estacionamientos'},
        ),
        migrations.AlterModelOptions(
            name='multa',
            options={'verbose_name': 'Multa', 'verbose_name_plural': 'Multas'},
        ),
        migrations.AlterModelOptions(
            name='reclamo',
            options={'verbose_name': 'Reclamo', 'verbose_name_plural': 'Reclamos'},
        ),
        migrations.AlterModelOptions(
            name='registrovisitantedepto',
            options={'verbose_name': 'Registro Visitante Depto', 'verbose_name_plural': 'Registros Visitante Depto'},
        ),
        migrations.AlterModelOptions(
            name='reservacion',
            options={'verbose_name': 'Reservación', 'verbose_name_plural': 'Reservaciones'},
        ),
        migrations.AlterModelOptions(
            name='residente',
            options={'verbose_name': 'Residente', 'verbose_name_plural': 'Residentes'},
        ),
        migrations.AlterModelOptions(
            name='respuesta',
            options={'verbose_name': 'Respuesta', 'verbose_name_plural': 'Respuestas'},
        ),
        migrations.AlterModelOptions(
            name='visitante',
            options={'verbose_name': 'Visitante', 'verbose_name_plural': 'Visitantes'},
        ),
        migrations.AlterField(
            model_name='adminempleadocontratada',
            name='run_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos', to='LifeBetterApp.empleado'),
        ),
        migrations.AlterField(
            model_name='adminempleadocontratada',
            name='rut_admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleados', to='LifeBetterApp.administracionexterna'),
        ),
        migrations.AlterField(
            model_name='administracionexterna',
            name='correo_admin',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='run_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anuncios', to='LifeBetterApp.empleado'),
        ),
        migrations.AlterField(
            model_name='bitacora',
            name='run_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bitacoras', to='LifeBetterApp.empleado'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='correo_empleado',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='encomienda',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='encomienda',
            name='run_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encomiendas', to='LifeBetterApp.empleado'),
        ),
        migrations.AlterField(
            model_name='encomienda',
            name='run_residente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encomiendas', to='LifeBetterApp.residente'),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='run_empleado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estacionamientos', to='LifeBetterApp.empleado'),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='run_residente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estacionamientos', to='LifeBetterApp.residente'),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='run_visitante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estacionamientos', to='LifeBetterApp.visitante'),
        ),
        migrations.AlterField(
            model_name='multa',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='multa',
            name='run_residente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multas', to='LifeBetterApp.residente'),
        ),
        migrations.AlterField(
            model_name='reclamo',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='reclamo',
            name='run_residente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reclamos', to='LifeBetterApp.residente'),
        ),
        migrations.AlterField(
            model_name='registrovisitantedepto',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='registrovisitantedepto',
            name='rut_residente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitas', to='LifeBetterApp.residente'),
        ),
        migrations.AlterField(
            model_name='registrovisitantedepto',
            name='rut_visitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros', to='LifeBetterApp.visitante'),
        ),
        migrations.AlterField(
            model_name='reservacion',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='reservacion',
            name='id_ec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservaciones', to='LifeBetterApp.espaciocomun'),
        ),
        migrations.AlterField(
            model_name='reservacion',
            name='run_residente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservaciones', to='LifeBetterApp.residente'),
        ),
        migrations.AlterField(
            model_name='residente',
            name='correo_residente',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='residente',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='id_reclamo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='LifeBetterApp.reclamo'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='run_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='LifeBetterApp.empleado'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LifeBetterApp.departamento'),
        ),
        migrations.AlterModelTable(
            name='adminempleadocontratada',
            table='admin_empleado_contratada',
        ),
        migrations.AlterModelTable(
            name='administracionexterna',
            table='administracion_externa',
        ),
        migrations.AlterModelTable(
            name='anuncio',
            table='anuncio',
        ),
        migrations.AlterModelTable(
            name='bitacora',
            table='bitacora',
        ),
        migrations.AlterModelTable(
            name='empleado',
            table='empleado',
        ),
        migrations.AlterModelTable(
            name='encomienda',
            table='encomienda',
        ),
        migrations.AlterModelTable(
            name='espaciocomun',
            table='espacio_comun',
        ),
        migrations.AlterModelTable(
            name='estacionamiento',
            table='estacionamiento',
        ),
        migrations.AlterModelTable(
            name='multa',
            table='multa',
        ),
        migrations.AlterModelTable(
            name='reclamo',
            table='reclamo',
        ),
        migrations.AlterModelTable(
            name='registrovisitantedepto',
            table='registro_visitante_depto',
        ),
        migrations.AlterModelTable(
            name='reservacion',
            table='reservacion',
        ),
        migrations.AlterModelTable(
            name='residente',
            table='residente',
        ),
        migrations.AlterModelTable(
            name='respuesta',
            table='respuesta',
        ),
        migrations.AlterModelTable(
            name='visitante',
            table='visitante',
        ),
    ]