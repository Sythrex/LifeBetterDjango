from django.urls import path

from . import views


urlpatterns = [
    
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('conserje/', views.conserje, name='conserje'),
    path('residente/', views.residente, name='residente'),
    # administrador
    path('admin/', views.admin, name='admin'),
    path('admin/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    
]
