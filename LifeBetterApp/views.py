import random
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transaction_commit_error import TransactionCommitError
from django.contrib.auth.decorators import login_required
from LifeBetterApp.forms import CrearDepartamentoForm, CrearUsuarioForm, EspacioComunForm, PagarGComunesForm, PagarGastosComunesForm, RegistroVisitanteDeptoForm, ReservacionForm, VisitanteForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Departamento, GastosComunes, User, Visitante, Residente, AdministracionExterna, Empleado, AdminEmpleadoContratada, RegistroVisitanteDepto, Multa, EspacioComun, Anuncio, Bitacora, Reservacion, Estacionamiento, Encomienda


## VISTAS DE PAGINAS PRINCIPALES
def index(request):
    return render(request, 'index.html', {})
def home(request):
    return render(request, 'sitio/home.html', {})
def servicio(request):
    return render(request, 'sitio/servicio.html', {})
def nosotros(request):
    return render(request, 'sitio/nosotros.html', {})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'adminedificio':
                return redirect('adminedificio')
            elif user.role == 'residente':
                return redirect('residente')
            elif user.role == 'conserje':
                return redirect('conserje')
            else:
                return redirect('home')
        else:
            # En caso de que la autenticación falle, puedes enviar un mensaje al template
            return render(request, "sitio/login.html", {'error': 'Nombre de usuario o contraseña incorrectos'})
    else:
        return render(request, "sitio/login.html")
def salir(request):
    logout(request)
    return redirect("home")

## VISTAS DE ERRORES
def unauthorized(request): 
    return render(request, 'errores/unauthorized.html', {})

# VISTAS DE AUTENTICACION
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

#VISTAS DE API WEBPAY
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
    print(f"Amount: {request.POST}")  # Agrega esta línea
    return_url = request.build_absolute_uri(reverse("webpay-plus-commit"))
    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }
    response = (Transaction()).create(buy_order, session_id, amount, return_url)
    return render(request,'webpay/plus/create.html', {
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

#RESIDENTE-----------------------------------------------------------------------------------------------
@login_required
def residente(request):
    if request.user.role == 'residente':
        residente = Residente.objects.all()
        context = {"residente":residente}
        return render(request, 'residente/residente.html', context)
    else:
        return redirect('unauthorized')
@login_required    
def perfil(request):
    if request.user.role == 'residente':
        perfil = Departamento.objects.all()
        context = {"perfil":perfil}
        return render(request, 'residente/perfil.html', context)
@login_required
def avisos(request):
    if request.user.role == 'residente':
        avi = Anuncio.objects.all()
        context ={"avisos": avi}
        return render(request, 'residente/avisos.html', context) 
@login_required       
def encoresidente(request):
    if request.user.role == 'residente':
        encom = Encomienda.objects.all()
        context ={"encom": encom}
    return render(request, 'residente/encoresidente.html', context)
@login_required
def espaciocomun(request):
    espacios = EspacioComun.objects.all()
    return render(request, 'residente/ecomun/espaciocomun.html', {'espacios': espacios})
@login_required
def listar_reservaciones(request):
    reservaciones = Reservacion.objects.filter(residente=request.user)
    return render(request, 'residente/ecomun/listar_reservaciones.html', {'reservaciones': reservaciones})
@login_required
def reservacion(request, id_reservacion):
    reserva = Reservacion.objects.get(id=id_reservacion)
    context = {"reserva": reserva}
    return render(request, 'residente/ecomun/reservacion.html', context)
@login_required
def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_reservaciones')
    else:
        form = ReservacionForm()
    return render(request, 'residente/ecomun/crear_reservacion.html', {'form': form})
@login_required
def gcomunes(request):
    form = PagarGComunesForm()
    context = {
        'form': form,
    }
    return render(request, 'sitio/gastoscomunes.html', context)
@login_required
def multasrev(request):
    return render(request, 'residente/multasrev.html', {})
@login_required
def reclamos(request):
    return render(request, 'residente/reclamos.html', {})
@login_required
def visitas(request):
    if request.user.role == 'residente':
        visi = Visitante.objects.all()
        context ={"visi": visi}
    return render(request, 'residente/visitas.html', context)


def resumen(request):
    return render(request, 'residente/resumen.html', {})
@login_required
def crear(request):
    return render(request, 'residente/crear/crear.html', {})

##ADMINISTRADOR------------------------------------------------------------------------------------------

@login_required
def admin(request):
    if request.user.role == 'adminedificio':
        adminedificio = Residente.objects.all()
        context = {"adminedificio":adminedificio}
        return render(request, 'administrador/adminedificio.html', context)
    else:
        return redirect('unauthorized')
    
@login_required
def admin(request):
    if request.user.role == 'adminedificio':
        adminedificio = Residente.objects.all()
        context = {"adminedificio":adminedificio}
        return render(request, 'administrador/adminedificio.html', context)
    else:
        return redirect('unauthorized')
    
@login_required
def crearusuario(request):
    if request.user.role == 'adminedificio':
        if request.method == 'POST':
            form = CrearUsuarioForm(request.POST)
            if form.is_valid():
                # Obtenemos la contraseña del formulario
                password = form.cleaned_data['password']
                # Hasheamos la contraseña antes de guardarla en la base de datos
                form.instance.password = make_password(password)
                # Guardamos el usuario en la base de datos
                form.save()
                return redirect('home')  # Redirigir a la página de inicio después de crear el usuario
        else:
            form = CrearUsuarioForm()
        return render(request, 'administrador/crearusuario.html', {'form': form})
    else:
        return redirect('unauthorized') 
      
@login_required
def creardepartamento(request):
    if request.user.role == 'adminedificio':
        if request.method == 'POST':
            form = CrearDepartamentoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('adminedificio')
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
            return redirect('listar_espacios_comunes')
    else:
        form = EspacioComunForm()
    return render(request, 'administrador/crear_ecomun.html', {'form': form})
def multasadmin(request):
    return render(request, 'administrador/multasadmin.html', {})

@login_required
def gastoscomunes(request):
    if request.method == 'POST':
        form = PagarGastosComunesForm(request.POST)
        if form.is_valid():
            mes = form.cleaned_data['mes']
            amount = form.cleaned_data['amount']
            print(f"Mes: {mes}, Amount: {amount}")  # Agrega esta línea
            return render(request, 'webpay/plus/create.html', {'form': form, 'amount': amount})  

    else:
        form = PagarGastosComunesForm()
    return render(request, 'sitio/gastoscomunes.html', {'form': form})

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
# CONSERJE------------------------------------------------------------------------------------------
@login_required
def conserje(request):
    if request.user.role == 'conserje':
        return render(request, 'conserje/conserje.html', {})
    else:
        return redirect('unauthorized')
def encomienda(request):
    return render(request, 'conserje/encomienda.html', {})
def bitacora(request):
    return render(request, 'conserje/bitacora.html', {})
def reclamos(request):
    return render(request, 'conserje/reclamos.html', {})
@login_required
def multa(request):
    if request.user.role == 'conserje':
        return render(request, 'conserje/multa.html', {})
    else:
        return redirect('unauthorized')
@login_required
def gestionencomienda(request):
    enco = encomienda.objects.all()
    context = {"enco": enco}
    return render(request, 'conserje/gestion/gestion.html', context)


@login_required
def visita(request):
    if request.user.role == 'conserje' or request.user.role == 'residente':     
        visitas = Visitante.objects.all()
        return render(request, 'conserje/visita.html', {'visitas': visitas})
    else:
        return redirect('unauthorized')   
    
@login_required
def editar_visita(request, id):
    if request.user.role == 'conserje' or request.user.role == 'residente':
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
    if request.user.role == 'conserje' or request.user.role == 'residente':
        visita = Visitante.objects.get(id=id)
        visita.delete()
        return redirect('visita')
    else:
        return redirect('unauthorized')

@login_required
def nueva_visita(request):
    if request.user.role == 'conserje' or request.user.role == 'residente':
        if request.method == 'POST':
            form1 = VisitanteForm(request.POST, prefix='form1')
            if form1.is_valid():
                form1.save()
                return redirect('visita')
        else:
            form1 = VisitanteForm(prefix='form1')
        return render(request, 'conserje/nuevavisita.html', {'form1': form1})
    else:
        return redirect('unauthorized')   
    
@login_required 
def registro_visitante_depto(request):
    if request.method == 'POST':
        form1 = RegistroVisitanteDeptoForm(request.POST, prefix='form1')
        if form1.is_valid():
            form1.save()
            return redirect('visita')
    else:
        form1 = RegistroVisitanteDeptoForm(prefix='form1')

    return render(request, 'conserje/agregarvisita.html', {'form1': form1})



