from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser, User
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
class Departamento(models.Model):
    id_depto = models.AutoField(primary_key=True)
    numero_depto = models.IntegerField()
    piso = models.IntegerField()

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return f'Departamento {self.numero_depto} - Piso {self.piso}'

class Residente(models.Model):
    rut_residente = models.CharField(primary_key=True, max_length=10)
    dvrun = models.CharField(max_length=1, validators=[validar_dv])
    pnombre_residente = models.CharField(max_length=50)
    snombre_residente = models.CharField(max_length=50, blank=True, null=True)
    appaterno_residente = models.CharField(max_length=50)
    apmaterno_residente = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento_residente = models.DateField()
    fecha_contrato_residente = models.DateField()
    correo_residente = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    fono_residente = models.CharField(max_length=15)
    tipo_residente = models.IntegerField()
    comite = models.BooleanField()
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'residente'
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def __str__(self):
        return f'{self.pnombre_residente} {self.appaterno_residente}'

class AdministracionExterna(models.Model):
    rut_admin = models.CharField(primary_key=True, max_length=10)
    nombre_admin = models.CharField(max_length=50)
    fecha_contrato_admin = models.DateField()
    correo_admin = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    fono_contacto_admin = models.CharField(max_length=15)

    class Meta:
        db_table = 'administracion_externa'
        verbose_name = 'Administración Externa'
        verbose_name_plural = 'Administraciones Externas'

    def __str__(self):
        return self.nombre_admin

class Empleado(models.Model):
    run_empleado = models.CharField(primary_key=True, max_length=10)
    dvrun_empleado = models.CharField(max_length=1, validators=[validar_dv])
    pnombre_empleado = models.CharField(max_length=50)
    snombre_empleado = models.CharField(max_length=50, blank=True, null=True)
    appaterno_empleado = models.CharField(max_length=50)
    apmaterno_empleado = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento_empleado = models.DateField()
    fecha_contrato_empleado = models.DateField()
    correo_empleado = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    fono_empleado = models.CharField(max_length=15)
    tipo_empleado = models.IntegerField()

    class Meta:
        db_table = 'empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f'{self.pnombre_empleado} {self.appaterno_empleado}'

class Visitante(models.Model):
    id = models.AutoField(primary_key=True)
    rut_visitante = models.CharField(max_length=8, validators=[validar_rut])
    dv_visitante = models.CharField(max_length=1, validators=[validar_dv])
    nombres_visitante = models.CharField(max_length=80)
    apellido_visitante = models.CharField(max_length=80)
    estacionamiento = models.BooleanField()
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'visitante'
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def __str__(self):
        return f'{self.nombres_visitante} {self.apellido_visitante}'

class AdminEmpleadoContratada(models.Model):
    id_admin_empleado_contratada = models.AutoField(primary_key=True)
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='contratos')
    rut_admin = models.ForeignKey(AdministracionExterna, on_delete=models.CASCADE, related_name='empleados')

    class Meta:
        db_table = 'admin_empleado_contratada'
        verbose_name = 'Admin Empleado Contratada'
        verbose_name_plural = 'Admin Empleados Contratadas'

    def __str__(self):
        return f'Contrato {self.id_admin_empleado_contratada}'

class RegistroVisitanteDepto(models.Model):
    id_visitante_depto = models.AutoField(primary_key=True)
    rut_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='registros')
    rut_residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='visitas')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registro_visitante_depto'
        verbose_name = 'Registro Visitante Depto'
        verbose_name_plural = 'Registros Visitante Depto'

    def __str__(self):
        return f'Registro {self.id_visitante_depto}'

class Multa(models.Model):
    id_multa = models.AutoField(primary_key=True)
    descripcion_multa = models.CharField(max_length=60)
    monto_multa = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_hora_multa = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='multas')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'multa'
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'

    def __str__(self):
        return f'Multa {self.id_multa}'

class EspacioComun(models.Model):
    id_ec = models.AutoField(primary_key=True)
    nombre_ec = models.CharField(max_length=60)
    descripcion_ec = models.CharField(max_length=60)
    capacidad_ec = models.IntegerField()

    class Meta:
        db_table = 'espacio_comun'
        verbose_name = 'Espacio Común'
        verbose_name_plural = 'Espacios Comunes'

    def __str__(self):
        return self.nombre_ec

class Anuncio(models.Model):
    id_asunto = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=60)
    contenido_asunto = models.CharField(max_length=60)
    fecha_hora_asunto = models.DateTimeField()
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='anuncios')

    class Meta:
        db_table = 'anuncio'
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'

    def __str__(self):
        return f'Anuncio {self.id_asunto}'

class Bitacora(models.Model):
    id_bitacora = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=60)
    contenido = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='bitacoras')

    class Meta:
        db_table = 'bitacora'
        verbose_name = 'Bitácora'
        verbose_name_plural = 'Bitácoras'

    def __str__(self):
        return f'Bitácora {self.id_bitacora}'

class Reservacion(models.Model):
    id_reservacion = models.AutoField(primary_key=True)
    estado_reservacion = models.CharField(max_length=20)
    inicio_fecha_hora_reservacion = models.DateTimeField()
    fin_fecha_hora_reservacion = models.DateTimeField()
    run_residente = models.ForeignKey('Residente', on_delete=models.CASCADE, related_name='reservaciones')
    id_ec = models.ForeignKey(EspacioComun, on_delete=models.CASCADE, related_name='reservaciones')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservacion'
        verbose_name = 'Reservación'
        verbose_name_plural = 'Reservaciones'

    def __str__(self):
        return f'Reservación {self.id_reservacion} - {self.espacio_comun.nombre_ec}'

class Estacionamiento(models.Model):
    id_estacionamiento = models.AutoField(primary_key=True)
    tipo_auto = models.IntegerField()
    patente = models.CharField(max_length=6)
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE, null=True, blank=True, related_name='estacionamientos')
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True, related_name='estacionamientos')
    run_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, null=True, blank=True, related_name='estacionamientos')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'estacionamiento'
        verbose_name = 'Estacionamiento'
        verbose_name_plural = 'Estacionamientos'

    def __str__(self):
        return f'Estacionamiento {self.id_estacionamiento}'

class Encomienda(models.Model):
    id_encomienda = models.AutoField(primary_key=True)
    estado_encomienda = models.CharField(max_length=20)
    fecha_hora_encomienda = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='encomiendas')
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='encomiendas')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'encomienda'
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'

    def __str__(self):
        return f'Encomienda {self.id_encomienda}'

class Reclamo(models.Model):
    id_reclamo = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=60)
    contenido_reclamo = models.CharField(max_length=200)
    fecha_hora_reclamo = models.DateTimeField()
    run_residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='reclamos')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reclamo'
        verbose_name = 'Reclamo'
        verbose_name_plural = 'Reclamos'

    def __str__(self):
        return f'Reclamo {self.id_reclamo}'

class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    contenido_respuesta = models.CharField(max_length=200)
    fecha_hora_respuesta = models.DateTimeField()
    id_reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE, related_name='respuestas')
    run_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='respuestas')

    class Meta:
        db_table = 'respuesta'
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return f'Respuesta {self.id_respuesta}'

class GastosComunes(models.Model):
    MESES = (
        ('Enero', 'Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
        ('Diciembre', 'Diciembre'),
    )

    mes = models.CharField(max_length=20, choices=MESES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mes} - ${self.amount}"

    mes = forms.ChoiceField(choices=MESES, widget=forms.Select(attrs={'class': 'form-control'}))