import requests
from django.contrib.auth.models import User

class CustomAuth:
    """
    Autenticación personalizada para validar usuarios a través de la API de Node.js.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            # Solicita datos al API
            api_url = "http://localhost:3000/usuarios"  # URL del endpoint
            response = requests.get(api_url)
            if response.status_code == 200:
                usuarios = response.json()
                usuario = next((u for u in usuarios if u['username'] == username and u['password'] == password), None)
                if usuario:
                    # Crear o recuperar el usuario en la base de datos local
                    user, created = User.objects.get_or_create(username=username)
                    if created:
                        # Opcional: asignar más datos al usuario si es necesario
                        user.first_name = usuario.get('first_name', '')
                        user.last_name = usuario.get('last_name', '')
                        user.save()
                    return user
        except Exception as e:
            print(f"Error autenticando: {e}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
