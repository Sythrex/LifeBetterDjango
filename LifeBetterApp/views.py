from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})

def home(request):
    return render(request, 'sitio/home.html', {})

def login(request):
    return render(request, 'sitio/login.html', {})

def admin(request):
    return render(request, 'administrador/index.html', {})

def conserje(request):
    return render(request, 'conserje/index.html', {})

def residente(request):
    return render(request, 'residente/index.html', {})
