from django.urls import path

from . import views


urlpatterns = [
    

    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('admin/', views.admin, name='admin'),
    path('conserje/', views.conserje, name='conserje'),
    path('residente/', views.residente, name='residente'),
    
]
