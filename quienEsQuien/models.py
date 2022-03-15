from django.db import models

# Create your models here.


class Usuarios(models.Model):
    nombre=models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    email = models.EmailField() # (blank=True, null=True) para dejar a un valor ser opcional
    contraseña = models.CharField(max_length=30)
    pruebaRealizada = models.BooleanField() # Si dentro del parentesis se pone verbose_name = "[nombre]", cambia el nombre que se le da en la pantalla de administrador

    class Meta:
        verbose_name='usuario'
        verbose_name_plural='usuarios'

    def __str__(self):
        return self.nombre