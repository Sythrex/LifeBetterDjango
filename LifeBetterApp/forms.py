from django import forms
from .models import Departamento, GastosComunes, Reclamo, User, Visitante, Residente, Empleado, RegistroVisitanteDepto, EspacioComun, Bitacora, Reservacion, Encomienda
from django.contrib.auth.forms import UserCreationForm


class PagarGastosComunesForm(forms.Form):

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

    mes = forms.ChoiceField(choices=MESES, widget=forms.Select(attrs={'class': 'form-control'}))

class PagarGComunesForm(forms.Form):
    mes = forms.ChoiceField(choices=[], label='Mes a Pagar', widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(label='Monto', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mes'].choices = GastosComunes.MESES

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password',]
    
class EncomiendaForm(forms.ModelForm):
        class Meta:
            model = Encomienda
            fields = ['estado_encomienda', 'fecha_hora_encomienda', 'run_residente', 'run_empleado', 'departamento']
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['run_residente'].queryset = Residente.objects.all()
            self.fields['run_empleado'].queryset = Empleado.objects.filter(role='conserje')
            self.fields['departamento'].queryset = Departamento.objects.all()

class ReclamoForm(forms.ModelForm):
    class Meta: 
        model = Reclamo
        fields =['asunto', 'contenido_reclamo']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un asunto'}),'contenido_reclamo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ingrese el detalle del reclamo o sugerencia'}),
    }

    def __init__(self, *args, **kwargs):
        super(ReclamoForm, self).__init__(*args, **kwargs)
        # Set hidden fields if needed (e.g., for logged-in user or department)
        # self.fields['run_residente'].widget = forms.HiddenInput()
        # self.fields['departamento'].widget = forms.HiddenInput()

class EspacioComunForm(forms.ModelForm):
    class Meta:
        model = EspacioComun
        fields = ['nombre_ec', 'descripcion_ec', 'capacidad_ec','estado_ec']

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['inicio_fecha_hora_reservacion', 'fin_fecha_hora_reservacion']

class RegistroVisitanteDeptoForm(forms.ModelForm):
    class Meta:
        model = RegistroVisitanteDepto
        fields = ['rut_visitante']

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['rut_visitante', 'dv_visitante', 'nombres_visitante', 'apellido_visitante', 'departamento','patente']

class CrearDepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['numero_depto', 'piso']


class CrearResidenteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Residente
        fields = [
            'rut_residente',
            'dvrun',
            'pnombre_residente',
            'snombre_residente',
            'appaterno_residente',
            'apmaterno_residente',
            'fecha_nacimiento_residente',
            'fecha_contrato_residente',
            'correo_residente',
            'fono_residente',
            'tipo_residente',
            'comite',
            'departamento',
        ]


class CrearBitacoraForm(forms.ModelForm):
    contenido = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Bitacora
        fields = ['id_bitacora', 'asunto', 'contenido', 'fecha_hora', 'empleado']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']

class CrearEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['run_empleado', 'dvrun_empleado', 'fecha_nacimiento_empleado', 'fecha_contrato_empleado', 'fono_empleado', 'sueldo_empleado']

