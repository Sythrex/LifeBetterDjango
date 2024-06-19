from django.urls import path, include
from django.urls import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('sitio/login/', views.login_view, name='login'),
    path('sitio/servicio/', views.servicio, name='servicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('conserje/', views.conserje, name='conserje'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),

    # Rutas para el restablecimiento de contraseña
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.done, name='done'),
    path('password_reset/<uidb64>/<token>/', views.confirm, name='confirm'),
    path('password_reset/done/', views.complete, name='complete'),

    # Gestion vista residente
    path('residente/', views.residente, name='residente'),
    path('avisos/', views.avisos, name='avisos'),
    path('encoresidente/', views.encoresidente, name='encoresidente'),
    path('perfil/', views.perfil, name='perfil'),
    path('residente/perfil/editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('reclamos/', views.reclamos, name='reclamos'),
    path('residente/crear/crear/', views.crear, name='crear'),
    path('residente/visita/', views.visita, name='visita_residente'),

    #CALENDAR
    path('residente/ecomun/espaciocomun/', views.espaciocomun, name='espaciocomun'),
    path('residente/ecomun/crear_reservacion/', views.crear_reservacion, name='crear_reservacion'),
    path('residente/ecomun/listar_reservaciones/', views.listar_reservaciones, name='listar_reservaciones'),
    path('residente/ecomun/detalle_espacio/<int:id_ec>/', views.detalle_espacio, name='detalle_espacio'),
    path('residente/ecomun/editar_reservacion/<int:id_reservacion>/', views.editar_reservacion, name='editar_reservacion'),
    path('residente/ecomun/eliminar_reservacion/<int:id_reservacion>/', views.eliminar_reservacion, name='eliminar_reservacion'),
    path('residente/ecomun/validar_disponibilidad/', views.validar_disponibilidad, name='validar_disponibilidad'),

    path('gcomunes/', views.gcomunes, name='gcomunes'),
    path('resumen/', views.resumen, name='resumen'),
    path('multasrev/', views.multasrev, name='multasrev'),
    # webpay
    path('webpay/plus/commit/', views.webpay_plus_commit, name='webpay-plus-commit'),
    path('webpay/plus/create/', views.webpay_plus_create, name='webpay-plus-create'),

    # administrador
    path('adminedificio/', views.admin, name='adminedificio'),
    path('administrador/crearusuario/', views.crearusuario, name='crearusuario'),
    path('administrador/residente/crear/', views.crear_residente, name='crear_residente'),
    path('administrador/creardepartamento/', views.creardepartamento, name='creardepartamento'),
    path('administrador/crear_ecomun/', views.crear_ecomun, name='crear_ecomun'),
    path('administrador/multasadmin/', views.multasadmin, name='multasadmin'),
    path('sitio/gastoscomunes/', views.gastoscomunes, name='gastoscomunes'),
    
    # GESTIÓN DE USUARIOS
    path('logout/', views.salir, name='logout'),  # Ruta para la vista de cerrar sesión

    # CONSERJE
    path('conserje/encomienda/', views.encomienda, name='encomienda'),
    path('conserje/visita/', views.visita, name='visita_conserje'),
    path('conserje/visita/crear', views.nueva_visita, name='nueva_visita'),
    path('conserje/registro/visita', views.registro_visitante_depto, name='registro_visitante_depto'),
    path('conserje/visita/salida_visita/<int:id>/', views.salida_visita, name='salida_visita'),
    path('conserje/visita/editar/<int:id>/', views.editar_visita, name='editar_visita'),
    path('conserje/visita/eliminar/<int:id>/', views.eliminar_visita, name='eliminar_visita'),
    path('conserje/multa/', views.multa, name='multa'),
    path('conserje/bitacora/', views.bitacora, name='bitacora'),
    path('conserje/bitacora/crear', views.crear_bitacora, name='crear_bitacora'),
    path('conserje/reclamos/', views.reclamos, name='reclamos'),


]
