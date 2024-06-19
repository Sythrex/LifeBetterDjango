from django import forms
from LifeBetterApp.models import Departamento, Empleado, Encomienda, Residente, User
from .models import Departamento, Empleado, Encomienda, RegistroVisitanteDepto, Residente, User, Reclamo,EspacioComun, Reservacion, GastosComunes, Visitante
from LifeBetterApp import models


class CrearUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')

    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password', 'departamento']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'role': 'Rol',
            'password': 'Contraseña',
            'departamento': 'Departamento',
        }
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),            
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PagarGastosComunesForm(forms.Form):
    mes = forms.ChoiceField(choices=[], label='Mes a Pagar', widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(label='Monto', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mes'].choices = GastosComunes.MESES

    
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
        fields = ['nombre_ec', 'descripcion_ec', 'capacidad_ec']

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['estado_reservacion', 'inicio_fecha_hora_reservacion', 'fin_fecha_hora_reservacion']

class RegistroVisitanteDeptoForm(forms.ModelForm):
    class Meta:
        model = RegistroVisitanteDepto
        fields = ['rut_visitante', 'rut_residente', 'departamento']

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['rut_visitante', 'dv_visitante', 'nombres_visitante', 'apellido_visitante', 'departamento']