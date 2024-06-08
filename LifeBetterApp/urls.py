from django.urls import path
from django.urls import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('sitio/login/', views.login, name='login'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('conserje/', views.conserje, name='conserje'),

    # Rutas para el restablecimiento de contraseña
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.done, name='done'),
    path('password_reset/<uidb64>/<token>/', views.confirm, name='confirm'),
    path('password_reset/done/', views.complete, name='complete'),


    # Gestion vista residente
    path('residente/', views.residente, name='residente'),
    path('avisos/', views.avisos, name='avisos'),
    path('encomienda/', views.encomienda, name='encomienda'),
    path('perfil/', views.perfil, name='perfil'),
    path('reclamos/', views.reclamos, name='reclamos'),
    path('visitas/', views.visitas, name='visitas'),
    path('gastoscomunes/', views.gastoscomunes, name='gastoscomunes'),

    # webpay
    path('webpay/plus/commit/', views.webpay_plus_commit, name='webpay-plus-commit'),
    path('webpay/plus/create/', views.webpay_plus_create, name='webpay-plus-create'),

    # administrador
    path('adminedificio/', views.admin, name='adminedificio'),
    path('administrador/crearusuario/', views.crear_usuario, name='crear_usuario'),
    
    # GESTIÓN DE USUARIOS
    path('logout/', views.salir, name='logout'),  # Ruta para la vista de cerrar sesión

    #Gestion de botones de conserje 
    path('conserje/encomienda/', views.encomienda, name='encomienda'),
    path('conserje/visita/', views.visita, name='visita'),
    path('conserje/multa/', views.multa, name='multa'),
]
