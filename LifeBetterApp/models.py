from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser): 
    Roles = (
        ('adminedificio', 'Administrador'),
        ('conserje', 'Conserje'),
        ('residente', 'Residente'),
    )
    role = models.CharField(max_length=100, choices=Roles, default='conserje')
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        