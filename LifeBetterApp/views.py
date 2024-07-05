from datetime import datetime
from django.utils import timezone
import random
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views, logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transaction_commit_error import TransactionCommitError
from django.contrib import messages


from .forms import (
    ActualizarPerfilForm, CambiarContrasenaForm, CrearBitacoraForm, CrearDepartamentoForm, CrearEmpleadoForm, EspacioComunForm,
    MultaForm, PagarGastosComunesForm, RegistroVisitanteDeptoForm, 
    ReservacionForm, UserForm, VisitanteForm, PerfilForm, CrearResidenteForm
)
from .models import (
    Bitacora, Departamento, GastosComunes, Multa, Visitante, Residente, RegistroVisitanteDepto, EspacioComun, Anuncio, Reservacion, 
    Encomienda, Empleado
)

# ================================================
#                VISTAS PRINCIPALES
# ================================================
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'sitio/home.html')

def servicio(request):
    return render(request, 'sitio/servicio.html')

def nosotros(request):
    return render(request, 'sitio/nosotros.html')

# ================================================
#          VISTAS DE AUTENTICACIÓN Y LOGIN
# ================================================
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(user.role)  # Redirige según el rol del usuario
        else:
            return render(request, 'sitio/login.html', {'error': 'Credenciales incorrectas'})
    else:
        return render(request, 'sitio/login.html')

def salir(request):
    logout(request)
    return redirect("home")

# Rutas para el restablecimiento de contraseña
def password_reset(request):
    return auth_views.PasswordResetView.as_view(
        template_name='password_reset/password_reset.html',
        email_template_name='password_reset/email.html',
        subject_template_name='password_reset/subject.txt',
        success_url=reverse_lazy('done')
    )(request)

def done(request):
    return auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset/done.html'
    )(request)

def confirm(request, uidb64=None, token=None):
    return auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset/confirm.html',
        success_url=reverse_lazy('complete')
    )(request, uidb64=uidb64, token=token)

def complete(request):
    return auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/complete.html'
    )(request)

## VISTAS DE ERRORES
def unauthorized(request): 
    return render(request, 'errores/unauthorized.html', {})

# ================================================
#                  VISTAS WEBPAY
# ================================================

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

@csrf_exempt
@require_http_methods(["POST"])
def webpay_plus_create(request):
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    mes = request.POST.get('mes')
    amount = VALOR_MESES.get(mes, 0)  # Obtén el valor de 'amount' basado en 'mes'
    return_url = request.build_absolute_uri(reverse("webpay-plus-commit"))
    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }
    response = (Transaction()).create(buy_order, session_id, amount, return_url)
    return render(request, 'webpay/plus/create.html', {
        'request': create_request,
        'response': response,
        'amount': amount,
    })

@csrf_exempt
@require_http_methods(["GET"])
def webpay_plus_commit(request):
    token = request.GET.get("token_ws") or request.GET.get("TBK_TOKEN")
    print("commit for token_ws: {}".format(token))
    try:
        response = (Transaction()).commit(token=token)
        print("response: {}".format(response))
    except TransactionCommitError as e:
        print("TransactionCommitError: {}".format(e.message))
        return render(request, 'webpay/plus/error.html', {'error': str(e)})
        
    return render(request, 'webpay/plus/commit.html', {'token': token, 'response': response})

# ================================================
#                 VISTAS RESIDENTE
# ================================================
#Dashboard
@login_required
def residente(request):
    if request.user.role == 'residente':
        try:
            residente = request.user.residente
            gastos_pendientes = GastosComunes.objects.filter(usuario=request.user, departamento=residente.departamento, estado='pendiente')
            anuncios = Anuncio.objects.all()  # O filtra por edificio si es necesario
            encomiendas = Encomienda.objects.filter(run_residente=residente)
            visitas = Visitante.objects.filter(departamento=residente.departamento)

            return render(request, 'residente/residente.html', {
                'usuario': request.user,
                'residente': residente,
                'gastos_pendientes': gastos_pendientes,
                'anuncios': anuncios,
                'encomiendas': encomiendas,
                'visitas': visitas,
            })
        except Residente.DoesNotExist:
            return redirect('unauthorized')  # Redirigir a una vista o página que maneje este error
    else:
        return redirect('unauthorized')
#Ver informacion del usuario y reedirige a editar
@login_required
def perfil(request):
    if request.user.role == 'residente':
        if request.method == 'POST':
            if 'cambiar_contrasena' in request.POST:
                contrasena_form = CambiarContrasenaForm(user=request.user, data=request.POST)
                if contrasena_form.is_valid():
                    contrasena_form.save()
                    return redirect('perfil')  # Redirigir después de cambiar la contraseña
            elif 'actualizar_perfil' in request.POST:
                perfil_form = ActualizarPerfilForm(instance=request.user, data=request.POST)
                if perfil_form.is_valid():
                    perfil_form.save()
                    return redirect('perfil')  # Redirigir después de actualizar el perfil
        else:
            contrasena_form = CambiarContrasenaForm(user=request.user)
            perfil_form = ActualizarPerfilForm(instance=request.user)
            return render(request, 'residente/perfil/perfil.html', {
                'contrasena_form': contrasena_form,
                'perfil_form': perfil_form,
            })
    else:
        return redirect('unauthorized')

@login_required
def editar_perfil(request):
    try:
        residente = request.user.reservaciones.first().run_residente 
    except AttributeError:
        residente = None  # Manejar el caso en que el usuario no tenga reservas

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)

            # Actualizar contraseña si se proporcionó
            nueva_contrasena = form.cleaned_data.get('password')
            if nueva_contrasena:
                usuario.password = make_password(nueva_contrasena)

            # Actualizar teléfono del residente (si es que es residente y se ha proporcionado un nuevo telefono)
            if residente:
                nuevo_telefono = request.POST.get('fono_residente')
                if nuevo_telefono:
                    residente.fono_residente = nuevo_telefono
                    residente.save()

            usuario.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)

    # Pasar el teléfono del residente al contexto (si existe)
    telefono_residente = residente.fono_residente if residente else None

    return render(request, 'residente/perfil/editar_perfil.html', {'form': form, 'telefono_residente': telefono_residente})

@login_required
def cambiar(request):
    if request.user.role == 'residente':
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Importante para mantener la sesión activa
                return redirect('perfil')  # O donde quieras redirigir después del cambio
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'residente/perfil/cambiar_contraseña.html', {'contrasena_form': form})

@login_required
def avisos(request):
    if request.user.role == 'residente':
        avi = Anuncio.objects.all()
        context = {"avisos": avi}
        return render(request, 'residente/avisos.html', context) 

@login_required
def encoresidente(request):
    if request.user.role == 'residente':
        encom = Encomienda.objects.filter(run_residente=request.user.residente)
        context = {"encom": encom}
        return render(request, 'residente/encoresidente.html', context)

@login_required
def gcomunes(request):
    if request.user.role == 'residente':
        gastos = GastosComunes.objects.filter(usuario=request.user)
        if request.method == 'POST':
            form = PagarGastosComunesForm(request.POST)
            if form.is_valid():
                mes = form.cleaned_data['mes']
                monto = VALOR_MESES.get(mes)  # Obtener monto desde el diccionario

                try:
                    gasto_comun = gastos.get(mes=mes)
                except GastosComunes.DoesNotExist:
                    gasto_comun = None
                
                if gasto_comun:
                    if gasto_comun.amount == monto:
                        # Procesar el pago aquí (por ejemplo, redirigir a Webpay Plus)
                        return redirect('webpay-plus-create', mes=mes)  # Reemplaza con tu URL
                    else:
                        form.add_error('amount', "El monto no coincide con el gasto común.")
                else:
                    form.add_error('mes', "No se encontró un gasto común para este mes.")
        else:
            form = PagarGastosComunesForm()
        context = {
            'gastos_comunes': gastos,
            'form': form
        }
    else:
        # Lógica para otros roles, por ejemplo, mostrar todos los gastos comunes para el administrador
        gastos = GastosComunes.objects.all()
        context = {'gastos_comunes': gastos}

    return render(request, 'sitio/gastoscomunes.html', context)

@login_required
def multasrev(request):
    return render(request, 'residente/multasrev.html', {})


@login_required
def visitas(request):
    if request.user.role == 'residente':
        visi = Visitante.objects.filter(departamento=request.user.residente.departamento)
        context = {"visi": visi}
        return render(request, 'residente/visitas.html', context)
    
@login_required
def crear(request):
    return render(request, 'residente/crear/crear.html', {})

# --------------------------- ESPACIO COMUN -------------------------- #
@login_required
def espaciocomun(request):
    espacios = EspacioComun.objects.all()
    reservas_por_espacio = {
        espacio.id_ec: Reservacion.objects.filter(id_ec=espacio)
        for espacio in espacios
    }
    return render(request, 'residente/ecomun/espaciocomun.html', {
        'espacios': espacios,
        'reservas_por_espacio': reservas_por_espacio,
    })

@login_required
def listar_reservaciones(request):
    if request.user.role == 'Residente':  
        reservaciones = Reservacion.objects.filter(run_residente__user=request.user)  
    else:
        reservaciones = Reservacion.objects.none()  # Si no es residente, no muestra reservas
    return render(request, 'residente/ecomun/listar_reservaciones.html', {'reservaciones': reservaciones})

@login_required
def reservacion(request, id_reservacion):
    reserva = get_object_or_404(Reservacion, id=id_reservacion)
    return render(request, 'residente/ecomun/reservacion.html', {"reserva": reserva})

@login_required
def crear_reservacion(request):
    espacios = EspacioComun.objects.all()
    reservas_por_espacio = {
        espacio.id_ec: Reservacion.objects.filter(id_ec=espacio)
        for espacio in espacios
    }
    return render(request, 'residente/ecomun/crear_reservacion.html', {
        'espacios': espacios,
        'reservas_por_espacio': reservas_por_espacio,
    })

@login_required
def detalle_espacio(request, id_ec):
    espacio = get_object_or_404(EspacioComun, id_ec=id_ec)
    reservas = Reservacion.objects.filter(id_ec=espacio)
    return render(request, 'residente/ecomun/detalle_espacio.html', {'espacio': espacio, 'reservas': reservas})

@login_required
def editar_reservacion(request, id_reservacion):
    reservacion = get_object_or_404(Reservacion, id=id_reservacion, run_residente=request.user.residente)
    if request.method == 'POST':
        form = ReservacionForm(request.POST, instance=reservacion)
        if form.is_valid():
            form.save()
            return redirect('listar_reservaciones')
    else:
        form = ReservacionForm(instance=reservacion)
    return render(request, 'residente/ecomun/editar_reservacion.html', {'form': form, 'reservacion': reservacion})

@login_required
def eliminar_reservacion(request, id_reservacion):
    reservacion = get_object_or_404(Reservacion, id=id_reservacion, run_residente=request.user.residente)
    if request.method == 'POST':
        reservacion.delete()
        return redirect('listar_reservaciones')
    return render(request, 'residente/ecomun/eliminar_reservacion.html', {'reservacion': reservacion})

@login_required
def validar_disponibilidad(request):
    espacio_id = request.GET.get('espacio_id')
    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')

    # Realiza la validación de disponibilidad (similar a la vista crear_reservacion)
    disponible = not Reservacion.objects.filter(
        id_ec=espacio_id,
        inicio_fecha_hora_reservacion__lt=fin,
        fin_fecha_hora_reservacion__gt=inicio
    ).exists()

    return JsonResponse({'disponible': disponible})

# ================================================
#                 VISTAS ADMINISTRADOR
# ================================================
@login_required
def admin(request):
    if request.user.role == 'adminedificio':
        # Aquí deberías obtener los datos que necesitas para la vista del administrador,
        total_residentes = Residente.objects.count()
        total_departamentos = Departamento.objects.count()
        total_empleados = Empleado.objects.count()
        residentes = Residente.objects.all()
        anuncios = Anuncio.objects.all()
        context = {
            'total_residentes': total_residentes,
            'total_departamentos': total_departamentos,
            'total_empleados': total_empleados,
            "residentes": residentes,
            "anuncios": anuncios,
        }
        return render(request, 'administrador/adminedificio.html', context)
    else:
        return redirect('unauthorized')

@login_required
def crear_empleado(request):
    if request.user.role == 'adminedificio':
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            empleado_form = CrearEmpleadoForm(request.POST)
            if user_form.is_valid() and empleado_form.is_valid():
                user = user_form.save()
                empleado = empleado_form.save(commit=False)
                empleado.usuario = user
                empleado.save()
                messages.success(request, 'Empleado creado exitosamente')
                return redirect('crear_empleado')
            else:
                messages.error(request, 'Error al crear el empleado')
        else:
            user_form = UserForm()
            empleado_form = CrearEmpleadoForm()
        return render(request, 'administrador/crear_empleado.html',{'user_form': user_form, 'empleado_form': empleado_form})
    else:
        return redirect('unauthorized')

@login_required
def crear_residente(request):
    if request.method == 'POST':
        form = CrearResidenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residente creado exitosamente')
            return redirect('crear_residente')
        else:
            messages.error(request, 'Error al crear el residente')
    else:
        form = CrearResidenteForm()
    return render(request, 'administrador/crear_residente.html', {'form': form})

@login_required
def creardepartamento(request):
    if request.user.role == 'adminedificio':
        if request.method == 'POST':
            form = CrearDepartamentoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Departamento creado exitosamente')
                return redirect('creardepartamento')
            else:
                messages.error(request, 'Error al crear el departamento')
        else:
            form = CrearDepartamentoForm()
        return render(request, 'administrador/creardepto.html', {'form': form})
    else:
        return redirect('unauthorized')

@login_required
def crear_ecomun(request):
    if request.method == 'POST':
        form = EspacioComunForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espacio común creado exitosamente')
            return redirect('crear_ecomun')
        else:
            messages.error(request, 'Error al crear el espacio común')
    else:
        form = EspacioComunForm()
    return render(request, 'administrador/crear_ecomun.html', {'form': form})

@login_required
def listar_espacios_comunes(request):
    espacios = EspacioComun.objects.all()
    return render(request, 'administrador/listar_espacios_comunes.html', {'espacios': espacios})

@login_required
def multasadmin(request):
    return render(request, 'administrador/multasadmin.html', {})

@login_required
def crear_multa(request):
    if request.method == 'POST':
        form = MultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Multa creada exitosamente')
            return redirect('multas')  # Redirige a la vista de multas
        else:
            messages.error(request, 'Error al crear la multa')
            
    else:
        form = MultaForm()
    return render(request, 'administrador/crear_multa.html', {'form': form})

@login_required
def gastoscomunes(request):
    if request.method == 'POST':
        form = PagarGastosComunesForm(request.POST)
        if form.is_valid():
            mes = form.cleaned_data['mes']
            amount = VALOR_MESES[mes]
            print(f"Mes: {mes}, Amount: {amount}")  # Agrega esta línea
            return render(request, 'webpay/plus/create.html', {'form': form, 'amount': amount})
    else:
        form = PagarGastosComunesForm()
    return render(request, 'sitio/gastoscomunes.html', {'form': form})

# ================================================
#                 VISTAS CONSERJE
# ================================================
@login_required
def conserje(request):
    if request.user.role == 'conserje':
        return render(request, 'conserje/conserje.html', {})
    else:
        return redirect('unauthorized')

@login_required
def encomienda(request):
    return render(request, 'conserje/encomienda.html', {})

@login_required
def reclamos(request):
    return render(request, 'conserje/reclamos.html', {})

@login_required
def multa(request):
    if request.user.role == 'adminedificio':
        multas = Multa.objects.all()
    else:
        # Suponiendo que el Empleado también tiene relación con el modelo User
        multas = Multa.objects.filter(run_empleado__user=request.user) 

    context = {'multas': multas}
    return render(request, 'multas.html', context)  # Asegúrate de tener la plantilla 'multas.html'

@login_required
def gestionencomienda(request):
    enco = Encomienda.objects.all()
    context = {"enco": enco}
    return render(request, 'conserje/gestion/gestion.html', context)

@login_required
def visita(request):
    if request.user.role in ['conserje', 'residente']:
        visitas = Visitante.objects.all()
        return render(request, 'conserje/visita.html', {'visitas': visitas})
    else:
        return redirect('unauthorized')

@login_required
def editar_visita(request, id):
    if request.user.role == 'conserje':
        visita = Visitante.objects.get(id=id)
        if request.method == 'POST':
            form1 = VisitanteForm(request.POST, instance=visita, prefix='form1')
            if form1.is_valid():
                form1.save()
                return redirect('visita')
        else:
            form1 = VisitanteForm(instance=visita, prefix='form1')
        return render(request, 'conserje/editarvisita.html', {'form1': form1})
    else:
        return redirect('unauthorized')

@login_required
def eliminar_visita(request, id):
    if request.user.role == 'conserje':
        visita = Visitante.objects.get(id=id)
        visita.delete()
        return redirect('visita_conserje')
    else:
        return redirect('unauthorized')

@login_required
def nueva_visita(request):
    if request.user.role == 'conserje':
        if request.method == 'POST':
            form1 = VisitanteForm(request.POST, prefix='form1')
            if form1.is_valid():
                form1.save()
                messages.success(request, 'Nueva visita creada exitosamente')
                return redirect('nueva_visita')
            else:
                messages.error(request, 'Error al crear la visita')

        else:
            form1 = VisitanteForm(prefix='form1')
        return render(request, 'conserje/nuevavisita.html', {'form1': form1})
    else:
        return redirect('unauthorized')

@login_required 
def registro_visitante_depto(request):
    if request.user.role in ['conserje', 'residente']:
        if request.method == 'POST':
            form1 = RegistroVisitanteDeptoForm(request.POST, prefix='form1')
            if form1.is_valid():
                form1.save()
                messages.success(request, 'Registro de visita creado exitosamente')
                return redirect('registro_visitante_depto')
            else:
                messages.error(request, 'Error al crear el registro de visita')

        else:
            form1 = RegistroVisitanteDeptoForm(prefix='form1')
        visitas = RegistroVisitanteDepto.objects.filter(fecha_hora_salida__isnull=True)
    else:
        return redirect('unauthorized')
    return render(request, 'conserje/agregarvisita.html', {'form1': form1, 'visitas': visitas})

@login_required
def salida_visita(request, id):
    if request.user.role == 'conserje':
        visita = RegistroVisitanteDepto.objects.get(id_visitante_depto=id)
        visita.fecha_hora_salida = datetime.now()
        visita.save()
        return redirect('registro_visitante_depto')
    else:
        return redirect('unauthorized')

@login_required    
def bitacora(request):
    if request.user.role in ['conserje', 'administrador']:
        bitacoras = Bitacora.objects.all()  # Obtener todas las bitácoras
        return render(request, 'conserje/bitacora.html', {'bitacoras': bitacoras})

@login_required    
def crear_bitacora(request):
    if request.user.role == 'conserje':
        if request.method == 'POST':
            form = CrearBitacoraForm(request.POST)
            if form.is_valid():
                bitacora_instance = form.save(commit=False)
                bitacora_instance.empleado = request.user.empleado
                bitacora_instance.save()
                messages.success(request, 'Bitácora creada exitosamente')
                return redirect('bitacora')
            else:
                messages.error(request, 'Error al crear la bitácora')

        else:
            form = CrearBitacoraForm()   
        return render(request, 'conserje/crearbitacora.html', {'form': form})
    else:
        return redirect('unauthorized')


@login_required
def vista_bitacoras(request):
    bitacoras = Bitacora.objects.all() 
    
    return render(request, 'bitacora.html', {'bitacoras': bitacoras})

@login_required
def marcar_salida_visita(request):
    if request.method == 'POST' and request.user.role == 'conserje':
        visita_id = request.POST.get('visita_id')
        visita = RegistroVisitanteDepto.objects.get(id=visita_id)
        visita.hora_salida = timezone.now()
        visita.save()
        return redirect('ruta_a_historial_visitas')
    else:
        return redirect('unauthorized')
