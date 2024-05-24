from django.shortcuts import render, redirect
#from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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
    return render(request, 'conserje/conserje.html', {})

def residente(request):
    return render(request, 'residente/residente.html', {})


## ADMINISTRADOR
def admin(request):
    return render(request, 'administrador/admin.html', {})

def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CrearUsuarioForm()
    return render(request, 'administrador/crearusuario.html', {'form': form})

## GESTIÓN DE ENSCOMIENDAS
@login_required
def gestioncur(request):
    cursos = cursos.objects.all()
    context = {"cursos": cursos}
    return render(request, 'gestion/gestioncur.html', context)


# GESTIÓN DE USUARIOS
def login(request):
    return render(request, "registration/login.html")

def salir(request):
    logout(request)
    return redirect("home")