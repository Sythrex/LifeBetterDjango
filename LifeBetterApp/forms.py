from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import (
    Departamento, Reclamo, User, Visitante, Residente, 
    Empleado, RegistroVisitanteDepto, EspacioComun, Bitacora, Reservacion, 
    Encomienda, Multa
)

# ================================================
#                FORMULARIOS DE USUARIO
# ================================================
class UsuarioForm(UserCreationForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'departamento', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'role': 'Rol',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
# ================================================
#            FORMULARIOS COMUNES
# ================================================

class PagarGastosComunesForm(forms.Form):
    VALOR_MESES = {
        'Enero': 100,
        'Febrero': 200,
        'Marzo': 300,
        'Abril': 400,
        'Mayo': 500,
        'Junio': 600,
        'Julio': 700,
        'Agosto': 800,
        'Septiembre': 900,
        'Octubre': 1000,
        'Noviembre': 1100,
        'Diciembre': 1200,
    }

    mes = forms.ChoiceField(
        choices=VALOR_MESES.items(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class MultaForm(forms.ModelForm):
    class Meta:
        model = Multa
        fields = ['run_residente', 'departamento', 'descripcion_multa', 'monto_multa', 'fecha_hora_multa']
        widgets = {
            'fecha_hora_multa': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Widget para fecha y hora
        }

# ================================================
#         FORMULARIOS   CONSERJE 
# ================================================
class RegistroVisitanteDeptoForm(forms.ModelForm):
    class Meta:
        model = RegistroVisitanteDepto
        fields = ['rut_visitante']

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['rut_visitante', 'dv_visitante', 'nombres_visitante', 'apellido_visitante', 'departamento','patente']

class CrearBitacoraForm(forms.ModelForm):
    contenido = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Bitacora
        fields = ['asunto', 'contenido', 'fecha_hora']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RegistroEncomiendaForm(forms.ModelForm):

    class Meta:
        model = Encomienda
        fields = ['nombre_encomienda', 'descripcion_encomienda', 'departamento','run_residente','run_empleado']
        widgets = {
            'estado_encomienda': forms.HiddenInput(),  # Campo oculto para estado_encomienda
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['estado_encomienda'] = 'pendiente'  # Establece el valor inicial como pendiente

class ReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['asunto', 'contenido_reclamo']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un asunto'}),
            'contenido_reclamo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ingrese el detalle'}),
        }
    def __init__(self, *args, **kwargs):
        super(ReclamoForm, self).__init__(*args, **kwargs)
        self.fields['run_residente'].widget = forms.HiddenInput()
        self.fields['departamento'].widget = forms.HiddenInput()

# ================================================
#         FORMULARIOS   ADMIN 
# ================================================
class CrearEcomun(forms.ModelForm):
    class Meta:
        model = EspacioComun
        fields = ['nombre_ec', 'descripcion_ec', 'capacidad_ec', 'estado_ec']
        widgets = {
            'nombre_ec': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del espacio'}),
            'descripcion_ec': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del espacio'}),
            'capacidad_ec': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad máxima'}),
            'estado_ec': forms.Select(attrs={'class': 'form-control'}, choices=EspacioComun.estado_ec), 
        }
        labels = {
            'nombre_ec': 'Nombre',
            'descripcion_ec': 'Descripción',
            'capacidad_ec': 'Capacidad',
            'estado_ec': 'Estado',
        }

class CrearResidenteForm(forms.ModelForm):
    fecha_nacimiento_residente = forms.DateField(
        label="Fecha de nacimiento",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_contrato_residente = forms.DateField(
        label="Fecha de Contrato",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    class Meta:
        model = Residente
        fields = [
            'rut_residente',
            'dvrun',
            'fecha_nacimiento_residente',
            'fecha_contrato_residente',
            'correo_residente',
            'fono_residente',
            'tipo_residente',
            'comite',
            'departamento'
        ]

class CrearEmpleadoForm(forms.ModelForm):
    fecha_contrato_empleado = forms.DateField(
            label="Fecha de Contrato",
            required=True,
            widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"]
        )
    fecha_nacimiento_empleado = forms.DateField(
        label="Fecha de nacimiento",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    class Meta:
        model = Empleado
        fields = ['run_empleado', 'dvrun_empleado', 'fecha_nacimiento_empleado', 'fecha_contrato_empleado', 'fono_empleado', 'sueldo_empleado']

class CrearDepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['numero_depto', 'piso']

# ================================================
#         FORMULARIOS   RESIDENTE
# ================================================
class ActualizarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class CambiarContrasenaForm(PasswordChangeForm):
    pass     

class EncomiendaResidenteForm(forms.ModelForm):
    class Meta:
        model = Encomienda
        fields = ['estado_encomienda', 'departamento']  # Campos relevantes para el residente
        widgets = {
            'estado_encomienda': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.HiddenInput(),  # Ocultar el departamento si es único
        }
        labels = {
            'estado_encomienda': 'Estado de la encomienda',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario = kwargs.get('initial', {}).get('usuario')  # Obtener el usuario del contexto

        # Si el usuario es un residente y tiene un solo departamento asociado, ocultarlo
        if usuario and usuario.role == 'residente':
            try:
                departamento = usuario.residente.departamento
                self.fields['departamento'].initial = departamento
                self.fields['departamento'].widget = forms.HiddenInput()
            except Residente.DoesNotExist:
                pass  # El usuario no tiene un residente asociado

class ReclamoForm(forms.ModelForm):
    class Meta: 
        model = Reclamo
        fields =['asunto', 'contenido_reclamo']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un asunto'}),
            'contenido_reclamo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ingrese el detalle del reclamo o sugerencia'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReclamoForm, self).__init__(*args, **kwargs)
        self.fields['run_empleado'].widget = forms.HiddenInput()

class EspacioComunForm(forms.ModelForm):
    class Meta:
        model = EspacioComun
        fields = ['nombre_ec', 'descripcion_ec', 'capacidad_ec','estado_ec']

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['inicio_fecha_hora_reservacion', 'fin_fecha_hora_reservacion']

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['rut_visitante', 'dv_visitante', 'nombres_visitante', 'apellido_visitante', 'departamento','patente']
