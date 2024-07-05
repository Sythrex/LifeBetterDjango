from django.urls import path
from django.urls import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ------------------------------------------------
    #                     SITIO
    # ------------------------------------------------
    path('', views.home, name='home'),
    path('sitio/login/', views.login_view, name='login'),
    path('sitio/servicio/', views.servicio, name='servicio'),
    path('nosotros/', views.nosotros, name='nosotros'),

    # ------------------------------------------------
    #             RESTABLECIMIENTO DE CONTRASEÑA
    # ------------------------------------------------
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.done, name='done'),
    path('password_reset/<uidb64>/<token>/', views.confirm, name='confirm'),
    path('password_reset/done/', views.complete, name='complete'),
    
    # ------------------------------------------------
    #                     WEBPAY
    # ------------------------------------------------
    path('webpay/plus/commit/', views.webpay_plus_commit, name='webpay-plus-commit'),
    path('webpay/plus/create/', views.webpay_plus_create, name='webpay-plus-create'),

    # ------------------------------------------------
    #                  RESIDENTE
    # ------------------------------------------------
    path('residente/', views.residente, name='residente'),
    path('cambiar/', views.cambiar, name='cambiar'),
    path('avisos/', views.avisos, name='avisos'),
    path('encoresidente/', views.encoresidente, name='encoresidente'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('reclamos/', views.reclamos, name='reclamos'),
    path('visitas/', views.visita, name='visita_residente'),
    path('crear/', views.crear, name='crear'), 
    path('gcomunes/', views.gcomunes, name='gcomunes'),
    path('multasrev/', views.multasrev, name='multasrev'),

    # ------------------------------------------------
    #                  ESPACIO COMUN
    # ------------------------------------------------
    path('residente/ecomun/', views.espaciocomun, name='espaciocomun'),
    path('residente/ecomun/crear_reservacion/', views.crear_reservacion, name='crear_reservacion'),# Aqui es donde estara el calendario
    path('residente/ecomun/listar_reservaciones/', views.listar_reservaciones, name='listar_reservaciones'),#Reservas hechas en el pasado
    path('residente/ecomun/detalle_espacio/<int:id_ec>/', views.detalle_espacio, name='detalle_espacio'),#Descripcion espacio
    path('residente/ecomun/editar_reservacion/<int:id_reservacion>/', views.editar_reservacion, name='editar_reservacion'),#Edicion de la reservacion
    path('residente/ecomun/eliminar_reservacion/<int:id_reservacion>/', views.eliminar_reservacion, name='eliminar_reservacion'),#Elimar reservacion
    path('residente/ecomun/validar_disponibilidad/', views.validar_disponibilidad, name='validar_disponibilidad'),#Valida disponibilidad

    # ------------------------------------------------
    #                 ADMINISTRADOR
    # ------------------------------------------------
    path('adminedificio/', views.admin, name='adminedificio'),
    path('adminedificio/residente/crear/', views.crear_residente, name='crear_residente'),
    path('adminedificio/empleado/crear/', views.crear_empleado, name='crear_empleado'),
    path('adminedificio/creardepartamento/', views.creardepartamento, name='creardepartamento'),
    path('adminedificio/crear_ecomun/', views.crear_ecomun, name='crear_ecomun'),
    path('listar_espacios_comunes/', views.listar_espacios_comunes, name='listar_espacios_comunes'),
    path('adminedificio/multasadmin/', views.multasadmin, name='multasadmin'),
    path('adminedificio/crear_multa/', views.crear_multa, name='crear_multa'),

    # ------------------------------------------------
    #                   CONSERJE
    # ------------------------------------------------
    path('conserje/', views.conserje, name='conserje'),
    path('encomienda/', views.encomienda, name='encomienda'),
    path('conserje/visita/', views.visita, name='visita_conserje'),
    path('conserje/visita/crear', views.nueva_visita, name='nueva_visita'),
    path('conserje/registro/visita', views.registro_visitante_depto, name='registro_visitante_depto'),
    path('marcar_salida/', views.marcar_salida_visita, name='marcar_salida'),
    path('conserje/visita/salida_visita/<int:id>/', views.salida_visita, name='salida_visita'),
    path('conserje/visita/editar/<int:id>/', views.editar_visita, name='editar_visita'),
    path('conserje/visita/eliminar/<int:id>/', views.eliminar_visita, name='eliminar_visita'),
    path('conserje/multa/', views.multa, name='multa'),
    path('conserje/bitacora/', views.bitacora, name='bitacora'),
    path('conserje/bitacora/crear', views.crear_bitacora, name='crear_bitacora'),
    path('ruta_bitacoras/', views.vista_bitacoras, name='vista_bitacoras'),


    # ------------------------------------------------
    #              GESTIÓN DE USUARIOS
    # ------------------------------------------------
    path('logout/', views.salir, name='logout'), 
    path('unauthorized/', views.unauthorized, name='unauthorized'),

]