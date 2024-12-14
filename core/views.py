from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm
from django.conf import settings
from pyrebase import pyrebase
from firebase_admin import auth as firebase_auth
from django.contrib.auth.models import User
import requests

# Inicializar Pyrebase
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
auth = firebase.auth()


# Vista de inicio
def inicio_view(request):
    return render(request, "inicio.html")


# Vista de Login con Firebase
def login_view(request):
    form = LoginForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            email = request.POST.get("username")  # Usamos el email como username
            password = request.POST.get("password")

            try:
                # Autenticación con Firebase
                firebase_user = auth.sign_in_with_email_and_password(email, password)
                id_token = firebase_user["idToken"]
                decoded_token = firebase_auth.verify_id_token(id_token)
                firebase_uid = decoded_token["uid"]

                # Sincronizar con Django User
                user, created = User.objects.get_or_create(
                    username=firebase_uid,
                    defaults={"email": email}
                )

                if created:
                    # Puedes agregar lógica para asignar roles u otros datos si se requiere
                    pass

                # Autenticamos al usuario en Django
                login(request, user)

                # Redirección según el rol (opcional, si manejas roles en Django o Firebase)
                role = decoded_token.get("role")  # Si tienes un custom claim "role" en Firebase
                print(f"Rol correspondiente del usuario es {role}")

            except Exception as e:
                messages.error(request, "Usuario o contraseña incorrectos.")
                print(f"Error de autenticación con Firebase: {e}")
        else:
            messages.error(request, "Formulario inválido.")
        return render(request, "login.html", {"form": form})
    return render(request, "login.html", {"form": form})


# Vista de Logout
def logout_view(request):
    logout(request)  # Elimina la sesión de Django
    return redirect("login")

