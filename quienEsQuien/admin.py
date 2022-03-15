from django.contrib import admin

from quienEsQuien.models import Usuarios
# Register your models here.


class UsuariosAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellidos", "email", "pruebaRealizada") # columnas que se mostraran antes de introducirme en el usuario
    search_fields = ("nombre", 'email') # podemos hacer busquedas por nombre e email
    list_filter = ("pruebaRealizada",) # podemos filtrar viendo si ha realizado o no la prueba

admin.site.register(Usuarios, UsuariosAdmin)