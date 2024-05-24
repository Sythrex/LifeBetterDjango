from django.shortcuts import render

from LifeBetterApp.forms import CrearUsuarioForm


def index(request):
    return render(request, 'index.html', {})

def home(request):
    return render(request, 'sitio/home.html', {})

def login(request):
    return render(request, 'sitio/login.html', {})

def nosotros(request):
    return render(request, 'sitio/nosotros.html', {})

def conserje(request):
    return render(request, 'conserje/index.html', {})

def residente(request):
    return render(request, 'residente/index.html', {})


## ADMINISTRADOR
def admin(request):
    return render(request, 'administrador/index.html', {})

def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CrearUsuarioForm()
    return render(request, 'administrador/crearusuario.html', {'form': form})

