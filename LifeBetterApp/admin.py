from django.contrib import admin
from .models import User, Visitante, Residente, AdministracionExterna, Empleado, AdminEmpleadoContratada, RegistroVisitanteDepto, Multa, EspacioComun, Anuncio, Bitacora, Reservacion, Estacionamiento, Encomienda

# Registra todos los modelos para que sean visibles en la admin
admin.site.register(User)
admin.site.register(Visitante)
admin.site.register(Residente)
admin.site.register(AdministracionExterna)
admin.site.register(Empleado)
admin.site.register(AdminEmpleadoContratada)
admin.site.register(RegistroVisitanteDepto)
admin.site.register(Multa)
admin.site.register(EspacioComun)
admin.site.register(Anuncio)
admin.site.register(Bitacora)
admin.site.register(Reservacion)
admin.site.register(Estacionamiento)
admin.site.register(Encomienda)