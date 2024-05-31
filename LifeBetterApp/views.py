import random
from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transaction_commit_error import TransactionCommitError
from transbank.error.transbank_error import TransbankError
from transbank.error.transaction_create_error import TransactionCreateError
from django.contrib.auth.decorators import login_required
from LifeBetterApp.forms import CrearUsuarioForm, PagarGastosComunesForm

def index(request):
    return render(request, 'index.html', {})

def home(request):
    return render(request, 'sitio/home.html', {})

def login(request):
    return render(request, 'sitio/login.html', {})

# Restablecimiento de contraseña con correo electronico
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


def nosotros(request):
    return render(request, 'sitio/nosotros.html', {})

def conserje(request):
    return render(request, 'conserje/conserje.html', {})

def residente(request):
    return render(request, 'residente/residente.html', {})

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

## ADMINISTRADOR
def admin(request):
    return render(request, 'administrador/adminedificio.html', {})

def crear_usuario(request):
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

## GESTIÓN DE ENCOMIENDAS
@login_required
def gestionencomienda(request):
    encomienda = encomienda.objects.all()
    context = {"encomienda": encomienda}
    return render(request, 'conserje/gestion/gestion.html', context)


# GESTIÓN DE USUARIOS
def login(request):
    return render(request, "sitio/login.html")

@login_required
def salir(request):
    logout(request)
    return redirect("home")

#Gestion de botones de conserje
def gestion(request):
    return render(request, 'conserje/gestion/gestion.html', {})
def editar(request):
    return render(request, 'conserje/gestion/editar.html', {})
def form(request):
    return render(request, 'conserje/gestion/form.html', {})
def crear(request):
    return render(request, 'conserje/gestion/crear.html', {})