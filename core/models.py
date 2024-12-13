from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now

# class Usuario(AbstractUser):
#     ROLE_CHOICES = [
#         ('alumno', 'Alumno'),
#         ('profesor', 'Profesor'),
#         ('director', 'Director'),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='alumno')
#     nombres = models.CharField(max_length=100, default="Sin nombre")
#     apellidos = models.CharField(max_length=100, default="Sin apellido")
#     rut = models.CharField(max_length=12, default="00000000-0")
#     direccion = models.CharField(max_length=200, default="Sin dirección")
#     fecha_nacimiento = models.DateField(null=True, blank=True)
#     telefono = models.CharField(max_length=15, default="000000000")
#     grado = models.CharField(max_length=50, blank=True, null=True)
#     especialidad = models.CharField(max_length=100, default="Sin especialidad")  # Nuevo campo

#     def __str__(self):
#         return f"{self.nombres} {self.apellidos}"


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