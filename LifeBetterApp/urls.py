from django.urls import path

from . import views


urlpatterns = [
    
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('conserje/', views.conserje, name='conserje'),
    path('residente/', views.residente, name='residente'),
    path('gastoscomunes/', views.gastoscomunes, name='gastoscomunes'),
    # webpay
    path('webpay/plus/commit/', views.webpay_plus_commit, name='webpay-plus-commit'),
    path('webpay/plus/create/', views.webpay_plus_create, name='webpay-plus-create'),
    # administrador
    path('admin/', views.admin, name='admin'),
    path('admin/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    
]
