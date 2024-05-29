from django.contrib import admin
from .models import User, Encomienda, EspacioComun, Visitante

# Register your models here.

admin.site.register(User)
admin.site.register(Encomienda)
admin.site.register(EspacioComun)
admin.site.register(Visitante)