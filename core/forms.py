from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Nota, Asignatura
import requests

# Formulario de inicio de sesión
from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField(label="Correo Electrónico", required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)


# Formulario para gestionar notas
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['alumno', 'asignatura', 'calificacion']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-control'}),
            'asignatura': forms.Select(attrs={'class': 'form-control'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para gestionar asignaturas
class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'descripcion', 'horario_inicio', 'horario_fin', 'profesor', 'sala']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'profesor': forms.Select(attrs={'class': 'form-control'}),
            'sala': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NotaFilterForm(forms.Form):
    asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        required=False,
        label="Asignatura",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    calificacion_min = forms.FloatField(
        required=False,
        label="Calificación mínima",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    calificacion_max = forms.FloatField(
        required=False,
        label="Calificación máxima",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
