from django.contrib import admin
from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('LifeBetterApp.urls')),  # Incluye las rutas de tu aplicación

    # Rutas para el restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='reset/password_reset.html',
        email_template_name='reset/password_reset_email.html',
        subject_template_name='reset/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')), 
        name='password_reset'),
]