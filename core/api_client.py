import requests
from .api_config import USERS_ENDPOINT, ASIGNATURAS_ENDPOINT, NOTAS_ENDPOINT

API_BASE_URL = "http://localhost:3000/api"

# Funciones para usuarios
def get_usuarios():
    """
    Llama a la API para obtener todos los usuarios.
    """
    url = f"{API_BASE_URL}/usuarios"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener usuarios: {response.status_code}, {response.text}")

def create_usuario(data):
    response = requests.post(USERS_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json()
    raise Exception(f"Error al crear usuario: {response.status_code}, {response.text}")

# Funciones para asignaturas
def create_asignatura(data):
    """
    Crea una nueva asignatura en la API de Node.js.
    """
    url = f"{API_BASE_URL}/asignaturas"
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return response.json()
    raise Exception(f"Error al crear asignatura: {response.status_code}, {response.text}")

def get_profesores():
    """
    Obtiene la lista de profesores desde la API de Node.js.
    """
    url = f"{API_BASE_URL}/usuarios?role=profesor"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Retorna solo los profesores
    raise Exception(f"Error al obtener profesores: {response.status_code}, {response.text}")

# Funciones para notas
def get_notas():
    try:
        response = requests.get('http://localhost:3000/api/notas')  # Cambia por tu URL de API
        response.raise_for_status()  # Levanta excepción si hay un error HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al obtener notas: {e}")

def create_nota(data):
    response = requests.post(NOTAS_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json()
    raise Exception(f"Error al crear nota: {response.status_code}, {response.text}")

def delete_usuario(usuario_id):
    """
    Elimina un usuario a través de la API de Node.js.
    :param usuario_id: ID del usuario a eliminar.
    :return: Respuesta de la API.
    """
    url = f"{USERS_ENDPOINT}/{usuario_id}"  # Construye la URL para la eliminación
    response = requests.delete(url)  # Realiza la solicitud DELETE
    if response.status_code == 200:
        return response.json()  # Devuelve la respuesta de la API si es exitosa
    else:
        raise Exception(f"Error al eliminar usuario: {response.status_code}, {response.text}")
    
def update_usuario(usuario_id, data):
    url = f"{USERS_ENDPOINT}/{usuario_id}"  # Construye la URL para actualizar
    response = requests.put(url, json=data)  # Realiza la solicitud PUT
    if response.status_code == 200:
        return response.json()  # Devuelve la respuesta de la API si es exitosa
    else:
        raise Exception(f"Error al actualizar usuario: {response.status_code}, {response.text}")
    
def get_usuario(usuario_id):
    url = f"{USERS_ENDPOINT}/{usuario_id}"  # Construye la URL para el usuario
    response = requests.get(url)  # Realiza la solicitud GET
    if response.status_code == 200:
        return response.json()  # Devuelve los datos del usuario
    else:
        raise Exception(f"Error al obtener usuario: {response.status_code}, {response.text}")
    
def buscar_usuarios(query):
    """
    Busca usuarios utilizando un parámetro de consulta en la API de Node.js.
    """
    url = f"{USERS_ENDPOINT}?search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error buscando usuarios: {response.status_code}, {response.text}")

def get_profesores():
    """
    Obtiene una lista de todos los profesores desde la API.
    """
    url = f"{USERS_ENDPOINT}?role=profesor"  # Filtra solo profesores
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al obtener profesores: {response.status_code}, {response.text}")

def get_asignaturas():
    response = requests.get(f'{API_BASE_URL}/asignaturas')
    if response.status_code == 200:
        return response.json()  # Devuelve la lista de asignaturas
    else:
        raise Exception(f"Error al obtener asignaturas: {response.status_code}, {response.text}")
    
def delete_asignatura(asignatura_id):
    response = requests.delete(f'{API_BASE_URL}/asignaturas/{asignatura_id}')
    if response.status_code != 200:
        raise Exception(f"Error al eliminar asignatura: {response.status_code}, {response.text}")
    
def update_asignatura(asignatura_id, data):
    response = requests.put(f'{API_BASE_URL}/asignaturas/{asignatura_id}', json=data)
    if response.status_code != 200:
        raise Exception(f"Error al actualizar asignatura: {response.status_code}, {response.text}")
    
def get_asignatura(asignatura_id):
    """
    Obtiene una asignatura específica desde la API.
    """
    response = requests.get(f'{API_BASE_URL}/asignaturas/{asignatura_id}')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener asignatura: {response.status_code}, {response.text}")
    
def login_usuario(username, password):
    url = 'http://localhost:3000/api/login'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error al iniciar sesión: {response.status_code}, {response.text}')
    
def create_nota(data):
    try:
        response = requests.post(f"{BASE_URL}/notas", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creando nota: {e}")
        return None
