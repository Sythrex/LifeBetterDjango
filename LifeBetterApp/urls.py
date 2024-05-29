from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sitio/login/', views.login, name='login'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('conserje/', views.conserje, name='conserje'),
    path('residente/', views.residente, name='residente'),
    path('gastoscomunes/', views.gastoscomunes, name='gastoscomunes'),

    # webpay
    path('webpay/plus/commit/', views.webpay_plus_commit, name='webpay-plus-commit'),
    path('webpay/plus/create/', views.webpay_plus_create, name='webpay-plus-create'),

    # administrador
    path('adminedificio/', views.admin, name='adminedificio'),
    path('admin/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    
    # GESTIÓN DE USUARIOS
    path('login', views.login, name='login'),  # Ruta para la vista de inicio de sesión
    path('salir', views.salir, name='salir'),  # Ruta para la vista de cerrar sesión
]