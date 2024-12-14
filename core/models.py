from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    horario_inicio = models.TimeField(default="08:00")  # Hora de inicio predeterminada
    horario_fin = models.TimeField(default="09:00")     # Hora de fin predeterminada
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'profesor'}
    )
    sala = models.CharField(max_length=50, default="Sin sala")  # Sala predeterminada

    def __str__(self):
        return self.nombre


class Nota(models.Model):
    alumno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    calificacion = models.FloatField()

    def __str__(self):
        return f"{self.alumno.username} - {self.asignatura.nombre} - {self.calificacion}"