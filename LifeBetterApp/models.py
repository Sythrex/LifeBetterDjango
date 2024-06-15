from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re


# Usuarios
class User(AbstractUser): 
    Roles = (
        ('adminedificio', 'Administrador'),
        ('conserje', 'Conserje'),
        ('residente', 'Residente'),
    )
    role = models.CharField(max_length=100, choices=Roles, default='adminedificio')

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

# Validaciones para RUT y DV
def validar_rut(value):
    """Valida que el valor ingresado sea un RUT válido."""
    if not re.match(r'^\d{1,8}$', value):
        raise ValidationError('%(value)s no es un RUT válido', params={'value': value})

def validar_dv(value):
    """Valida que el valor ingresado sea un dígito verificador válido."""
    if not re.match(r'^[\dkK]$', value):
        raise ValidationError('%(value)s no es un dígito verificador válido', params={'value': value})

# Modelos basados en las tablas SQL proporcionadas
#16
class Departamento(models.Model):
    id_depto = models.AutoField(primary_key=True)
    numero_depto = models.IntegerField()
    piso = models.IntegerField()

    class Meta:
        db_table = 'departamento'

#1
class Residente(models.Model):
    rut_residente = models.CharField(primary_key=True, max_length=10)
    dvrun = models.CharField(max_length=1, validators=[validar_dv])
    pnombre_residente = models.CharField(max_length=50)
    snombre_residente = models.CharField(max_length=50, blank=True, null=True)
    appaterno_residente = models.CharField(max_length=50)
    apmaterno_residente = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento_residente = models.DateField()
    fecha_contrato_residente = models.DateField()
    correo_residente = models.EmailField(max_length=50, blank=True, null=True)
    fono_residente = models.CharField(max_length=15)
    tipo_residente = models.IntegerField()
    comite = models.BooleanField()
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.rut_residente

#2
class AdministracionExterna(models.Model):
    rut_admin = models.CharField(primary_key=True, max_length=10)
    nombre_admin = models.CharField(max_length=50)
    fecha_contrato_admin = models.DateField()
    correo_admin = models.EmailField(max_length=50, blank=True, null=True)
    fono_contacto_admin = models.CharField(max_length=15)

    def __str__(self):
        return self.rut_admin

#3
class Empleado(models.Model):
    run_empleado = models.CharField(primary_key=True, max_length=10)
    dvrun_empleado = models.CharField(max_length=1, validators=[validar_dv])
    pnombre_empleado = models.CharField(max_length=50)
    snombre_empleado = models.CharField(max_length=50, blank=True, null=True)
    appaterno_empleado = models.CharField(max_length=50)
    apmaterno_empleado = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento_empleado = models.DateField()
    fecha_contrato_empleado = models.DateField()
    correo_empleado = models.EmailField(max_length=50, blank=True, null=True)
    fono_empleado = models.CharField(max_length=15)
    tipo_empleado = models.IntegerField()

    def __str__(self):
        return self.run_empleado

#4
class Visitante(models.Model):
    rut_visitante = models.CharField(primary_key=True, max_length=8, validators=[validar_rut])
    dv_visitante = models.CharField(max_length=1, validators=[validar_dv])
    nombres_visitante = models.CharField(max_length=80)
    apellido_visitante = models.CharField(max_length=80)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.rut_visitante}-{self.dv_visitante}'

#5
class AdminEmpleadoContratada(models.Model):
    id_admin_empleado_contratada = models.AutoField(primary_key=True)
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    rut_admin = models.ForeignKey(AdministracionExterna, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_admin_empleado_contratada)

#6
class RegistroVisitanteDepto(models.Model):
    id_visitante_depto = models.AutoField(primary_key=True)
    rut_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)
    rut_residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.id_visitante_depto)

#7
class Multa(models.Model):
    id_multa = models.AutoField(primary_key=True)
    descripcion_multa = models.CharField(max_length=60)
    monto_multa = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_hora_multa = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.id_multa)

#8
class EspacioComun(models.Model):
    id_ec = models.AutoField(primary_key=True)
    nombre_ec = models.CharField(max_length=60)
    descripcion_ec = models.CharField(max_length=60)
    capacidad_ec = models.IntegerField()

    def __str__(self):
        return self.nombre_ec

#9
class Anuncio(models.Model):
    id_asunto = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=60)
    contenido_asunto = models.CharField(max_length=60)
    fecha_hora_asunto = models.DateTimeField()
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_asunto)

#10
class Bitacora(models.Model):
    id_bitacora = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=60)
    contenido = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_bitacora)

#11
class Reservacion(models.Model):
    id_reservacion = models.AutoField(primary_key=True)
    estado_reservacion = models.CharField(max_length=20)
    inicio_fecha_hora_reservacion = models.DateTimeField()
    fin_fecha_hora_reservacion = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    id_ec = models.ForeignKey(EspacioComun, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.id_reservacion)

#12
class Estacionamiento(models.Model):
    id_estacionamiento = models.AutoField(primary_key=True)
    tipo_auto = models.IntegerField()
    patente = models.CharField(max_length=6)
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE, null=True, blank=True)
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    run_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.id_estacionamiento)

#13
class Encomienda(models.Model):
    id_encomienda = models.AutoField(primary_key=True)
    estado_encomienda = models.CharField(max_length=20)
    fecha_hora_encomienda = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.id_encomienda)
    
#14
class Reclamo(models.Model):
    id_reclamo = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=60)
    contenido_reclamo = models.CharField(max_length=200)
    fecha_hora_reclamo = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.id_reclamo)
    
#15
class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    contenido_respuesta = models.CharField(max_length=200)
    fecha_hora_respuesta = models.DateTimeField()
    id_reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE)
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_respuesta)