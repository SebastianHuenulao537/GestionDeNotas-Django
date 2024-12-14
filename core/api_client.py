import requests

# Configuración base de la API
API_BASE_URL = "http://localhost:3000/api"

USERS_ENDPOINT = f"{API_BASE_URL}/usuarios"
ASIGNATURAS_ENDPOINT = f"{API_BASE_URL}/asignaturas"
NOTAS_ENDPOINT = f"{API_BASE_URL}/notas"

# -------------------------------
# Funciones para Usuarios
# -------------------------------

def get_usuarios():
    """
    Obtiene todos los usuarios desde la API.
    """
    response = requests.get(USERS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener usuarios: {response.status_code}, {response.text}")

def create_usuario(data):
    """
    Crea un usuario en la API.
    """
    response = requests.post(USERS_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json()
    raise Exception(f"Error al crear usuario: {response.status_code}, {response.text}")

def get_usuario(usuario_id):
    """
    Obtiene los datos de un usuario específico.
    """
    url = f"{USERS_ENDPOINT}/{usuario_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener usuario: {response.status_code}, {response.text}")

def update_usuario(usuario_id, data):
    """
    Actualiza un usuario específico.
    """
    url = f"{USERS_ENDPOINT}/{usuario_id}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al actualizar usuario: {response.status_code}, {response.text}")

def delete_usuario(usuario_id):
    """
    Elimina un usuario específico.
    """
    url = f"{USERS_ENDPOINT}/{usuario_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al eliminar usuario: {response.status_code}, {response.text}")

def buscar_usuarios(query):
    """
    Busca usuarios por un término específico.
    """
    url = f"{USERS_ENDPOINT}?search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error buscando usuarios: {response.status_code}, {response.text}")

def get_profesores():
    """
    Obtiene la lista de profesores.
    """
    url = f"{USERS_ENDPOINT}?role=profesor"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener profesores: {response.status_code}, {response.text}")

# -------------------------------
# Funciones para Asignaturas
# -------------------------------

def get_asignaturas():
    """
    Obtiene todas las asignaturas.
    """
    response = requests.get(ASIGNATURAS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener asignaturas: {response.status_code}, {response.text}")

def create_asignatura(data):
    """
    Crea una nueva asignatura.
    """
    response = requests.post(ASIGNATURAS_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json()
    raise Exception(f"Error al crear asignatura: {response.status_code}, {response.text}")

def get_asignatura(asignatura_id):
    """
    Obtiene una asignatura específica.
    """
    url = f"{ASIGNATURAS_ENDPOINT}/{asignatura_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener asignatura: {response.status_code}, {response.text}")

def update_asignatura(asignatura_id, data):
    """
    Actualiza una asignatura específica.
    """
    url = f"{ASIGNATURAS_ENDPOINT}/{asignatura_id}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al actualizar asignatura: {response.status_code}, {response.text}")

def delete_asignatura(asignatura_id):
    """
    Elimina una asignatura específica.
    """
    url = f"{ASIGNATURAS_ENDPOINT}/{asignatura_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al eliminar asignatura: {response.status_code}, {response.text}")

# -------------------------------
# Funciones para Notas
# -------------------------------

def get_notas():
    """
    Obtiene todas las notas.
    """
    response = requests.get(NOTAS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener notas: {response.status_code}, {response.text}")

def create_nota(data):
    """
    Crea una nueva nota.
    """
    response = requests.post(NOTAS_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json()
    raise Exception(f"Error al crear nota: {response.status_code}, {response.text}")

def update_nota(nota_id, data):
    """
    Actualiza una nota específica.
    """
    url = f"{NOTAS_ENDPOINT}/{nota_id}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al actualizar nota: {response.status_code}, {response.text}")

def delete_nota(nota_id):
    """
    Elimina una nota específica.
    """
    url = f"{NOTAS_ENDPOINT}/{nota_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al eliminar nota: {response.status_code}, {response.text}")
