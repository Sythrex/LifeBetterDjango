import random
from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse
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
            form.save()
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

## GESTIÓN DE ENSCOMIENDAS
@login_required
def gestioncur(request):
    cursos = cursos.objects.all()
    context = {"cursos": cursos}
    return render(request, 'gestion/gestioncur.html', context)


# GESTIÓN DE USUARIOS
def login(request):
    return render(request, "sitio/login.html")

@login_required
def salir(request):
    logout(request)
    return redirect("home")