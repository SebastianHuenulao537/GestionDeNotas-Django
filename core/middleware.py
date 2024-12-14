from django.contrib.auth.models import User
from django.contrib.auth import login
from firebase_admin import auth as firebase_auth

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        id_token = request.headers.get("Authorization")  # Token de Firebase desde el cliente

        if id_token:
            try:
                decoded_token = firebase_auth.verify_id_token(id_token)
                firebase_uid = decoded_token['uid']
                email = decoded_token.get('email', '')

                # Sincroniza usuario de Firebase con Django
                user, created = User.objects.get_or_create(
                    username=firebase_uid,
                    defaults={'email': email}
                )

                # Autentica al usuario en Django
                if user:
                    login(request, user)

            except Exception as e:
                print(f"Error autenticando con Firebase: {e}")

        return self.get_response(request)
