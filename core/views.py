from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
import requests


# Create your views here.
def inicio_view(request):
    return render(request, "inicio.html")

def login_view(request):
    form = LoginForm(data=request.POST)
    if request.method == "POST":
        print(form.is_valid())
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            if username and password:
                # URL de la API para obtener usuarios
                api_url = "http://localhost:3000/api/usuarios"
                try:
                    response = requests.get(api_url)
                    if response.status_code == 200:
                        usuarios = response.json()
                        usuario = next(
                            (
                                u
                                for u in usuarios
                                if u["username"] == username
                                and u["password"] == password
                            ),
                            None,
                        )
                        print(usuario)
                        if not usuario:
                            print("Usuario o contraseña incorrectos.")
                    else:
                        print("No se pudo conectar al servidor. Intenta más tarde.")
                except requests.exceptions.RequestException as e:
                    print(f"Error de conexión: {e}")
        return render(request, "login.html", {"form": form})
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def alumno_dashboard(request):
    try:
        # Obtener el `username` del alumno desde la sesión del usuario
        alumno_username = request.user.username

        # Llamar a la API de Node.js para obtener las notas
        response = requests.get(
            f"http://localhost:3000/api/notas/alumno/{alumno_username}"
        )
        response.raise_for_status()  # Genera una excepción si hay un error

        # Procesar las notas devueltas por la API
        notas = response.json()
        return render(request, "alumno_dashboard.html", {"notas": notas})
    except requests.exceptions.RequestException as e:
        return render(request, "error.html", {"error": f"Error al obtener notas: {e}"})


# Dashboard para profesores


def profesor_dashboard(request):
    try:
        profesor_id = request.user.username
        response = requests.get(
            f"http://localhost:3000/api/notas/profesor/{profesor_id}"
        )
        response.raise_for_status()

        notas = response.json()

        # Filtrar por búsqueda si se especifica
        query = request.GET.get("search", "").lower()
        if query:
            notas = [
                nota
                for nota in notas
                if query in nota.get("alumno_nombre", "").lower()
                or query in nota.get("asignatura_nombre", "").lower()
            ]

        return render(
            request,
            "profesor_dashboard.html",
            {
                "notas": notas,
                "profesor": request.user,
            },
        )
    except requests.exceptions.RequestException as e:
        return render(request, "error.html", {"error": f"Error al obtener notas: {e}"})


# Función para agregar una nota


def agregar_nota(request):
    try:
        alumnos = requests.get("http://localhost:3000/api/usuarios").json()
        asignaturas = requests.get("http://localhost:3000/api/asignaturas").json()

        if request.method == "POST":
            data = {
                "alumno": request.POST.get("alumno"),
                "asignatura": request.POST.get("asignatura"),
                "calificacion": request.POST.get("calificacion"),
                "profesor": request.user.username,
            }
            response = requests.post("http://localhost:3000/api/notas", json=data)
            if response.status_code == 201:
                messages.success(request, "Nota creada correctamente.")
                return redirect("profesor_dashboard")

        return render(
            request,
            "agregar_nota.html",
            {"alumnos": alumnos, "asignaturas": asignaturas},
        )
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Función para editar una nota


def editar_nota(request, nota_id):
    try:
        # Obtener la nota desde la API
        response = requests.get(f"http://localhost:3000/api/notas/{nota_id}")
        if response.status_code != 200:
            raise Exception(
                f"Error al obtener la nota: {response.json().get('message')}"
            )

        nota = response.json()  # Datos actuales de la nota

        if request.method == "POST":
            # Actualizar datos desde el formulario
            data = {
                "alumno": request.POST.get("alumno"),
                "asignatura": request.POST.get("asignatura"),
                "calificacion": request.POST.get("calificacion"),
                "profesor": request.user.username,  # Profesor que edita la nota
            }
            update_response = requests.put(
                f"http://localhost:3000/api/notas/{nota_id}", json=data
            )
            if update_response.status_code == 200:
                messages.success(request, "Nota actualizada correctamente.")
                return redirect("profesor_dashboard")
            else:
                raise Exception(
                    f"Error al actualizar la nota: {update_response.json().get('message')}"
                )

        # Obtener alumnos y asignaturas para mostrar en el formulario
        alumnos_response = requests.get("http://localhost:3000/api/usuarios")
        asignaturas_response = requests.get("http://localhost:3000/api/asignaturas")

        alumnos = [
            alumno for alumno in alumnos_response.json() if alumno["role"] == "alumno"
        ]
        asignaturas = asignaturas_response.json()

        return render(
            request,
            "editar_nota.html",
            {
                "nota": nota,
                "alumnos": alumnos,
                "asignaturas": asignaturas,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Función para eliminar una nota


def eliminar_nota(request, nota_id):
    try:
        if request.method == "POST":
            # Llamar a la API para eliminar la nota
            response = requests.delete(f"http://localhost:3000/api/notas/{nota_id}")
            if response.status_code == 200:
                messages.success(request, "Nota eliminada correctamente.")
            else:
                raise Exception(
                    f"Error al eliminar la nota: {response.json().get('message')}"
                )
        return redirect("profesor_dashboard")
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Dashboard para directores


def director_dashboard(request):
    try:
        # Obtén las asignaturas desde la API
        asignaturas = get_asignaturas()

        # Obtén los usuarios desde la API
        usuarios = get_usuarios()
        alumnos = [usuario for usuario in usuarios if usuario["role"] == "alumno"]
        profesores = [usuario for usuario in usuarios if usuario["role"] == "profesor"]

        return render(
            request,
            "director_dashboard.html",
            {
                "asignaturas": asignaturas,
                "alumnos": alumnos,
                "profesores": profesores,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Función para agregar una asignatura


def agregar_asignatura(request):
    try:
        # Obtén la lista de profesores desde la API
        profesores = get_profesores()

        if request.method == "POST":
            # Obtener el ID del profesor seleccionado
            profesor_id = request.POST.get("profesor")
            # Buscar el nombre del profesor en la lista de profesores
            profesor_nombre = next(
                (
                    profesor["nombres"] + " " + profesor["apellidos"]
                    for profesor in profesores
                    if profesor["id"] == profesor_id
                ),
                "",
            )

            # Preparar los datos para enviar a la API
            data = {
                "nombre": request.POST.get("nombre"),
                "descripcion": request.POST.get("descripcion"),
                "horario_inicio": request.POST.get("horario_inicio"),
                "horario_fin": request.POST.get("horario_fin"),
                "profesor": profesor_nombre,  # Guardar el nombre del profesor en lugar de su ID
                "sala": request.POST.get("sala"),
            }

            # Llamar a la API para crear la asignatura
            create_asignatura(data)
            messages.success(request, "Asignatura creada correctamente.")
            return redirect("director_dashboard")

        return render(request, "agregar_asignatura.html", {"profesores": profesores})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Función para editar una asignatura


def editar_asignatura(request, asignatura_id):
    try:
        # Obtén los datos de la asignatura desde la API
        asignatura = get_asignatura(asignatura_id)
        if request.method == "POST":
            # Actualiza los datos de la asignatura con los valores del formulario
            data = {
                "nombre": request.POST.get("nombre"),
                "descripcion": request.POST.get("descripcion"),
                "horario_inicio": request.POST.get("horario_inicio"),
                "horario_fin": request.POST.get("horario_fin"),
                "profesor": request.POST.get("profesor"),
                "sala": request.POST.get("sala"),
            }
            update_asignatura(
                asignatura_id, data
            )  # Llama a la API para guardar los cambios
            messages.success(
                request,
                f"La asignatura {data['nombre']} fue actualizada correctamente.",
            )
            return redirect("director_dashboard")

        return render(request, "editar_asignatura.html", {"asignatura": asignatura})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Función para eliminar una asignatura


def eliminar_asignatura(request, asignatura_id):
    if request.method == "POST":
        try:
            # Llama a la API para eliminar la asignatura
            delete_asignatura(asignatura_id)
            messages.success(request, "Asignatura eliminada correctamente.")
            return redirect("director_dashboard")
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})
    return render(request, "eliminar_asignatura.html", {"asignatura_id": asignatura_id})


# Función para agregar un usuario


def agregar_usuario(request):
    if request.method == "POST":
        try:
            data = {
                "username": request.POST.get("username"),
                "password": request.POST.get("password"),
                "role": request.POST.get("role"),
                "nombres": request.POST.get("nombres"),
                "apellidos": request.POST.get("apellidos"),
                "rut": request.POST.get("rut"),
                "direccion": request.POST.get("direccion"),
                "telefono": request.POST.get("telefono"),
                "especialidad": request.POST.get("especialidad"),
            }
            create_usuario(data)
            return redirect("director_dashboard")
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})
    return render(request, "agregar_usuario.html")


# Función para editar un usuario


def editar_usuario(request, usuario_id, role):
    try:
        # Obtén el usuario desde la API
        usuario = get_usuario(usuario_id)
        if usuario["role"] != role:
            return render(
                request, "error.html", {"error": f"El usuario no tiene el rol {role}"}
            )

        if request.method == "POST":
            # Actualiza los datos del usuario
            data = {
                "nombres": request.POST.get("nombres"),
                "apellidos": request.POST.get("apellidos"),
                "rut": request.POST.get("rut"),
                "direccion": request.POST.get("direccion"),
                "telefono": request.POST.get("telefono"),
            }
            if role == "alumno":
                data["grado"] = request.POST.get("grado")
            elif role == "profesor":
                data["especialidad"] = request.POST.get("especialidad")
            update_usuario(usuario_id, data)
            messages.success(request, f"Usuario {role} actualizado correctamente.")
            return redirect("director_dashboard")

        return render(request, f"editar_{role}.html", {"usuario": usuario})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


# Función para eliminar un usuario


def eliminar_usuario(request, usuario_id):
    if request.method == "POST":
        try:
            delete_usuario(usuario_id)
            messages.success(request, "Usuario eliminado correctamente.")
            return redirect("director_dashboard")
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})
    return render(request, "eliminar_usuario.html", {"usuario_id": usuario_id})


def editar_alumno(request, usuario_id):
    try:
        # Obtén los datos del alumno desde la API
        usuario = get_usuario(usuario_id)
        if request.method == "POST":
            # Actualiza los datos del alumno con los valores del formulario
            data = {
                "nombres": request.POST.get("nombres"),
                "apellidos": request.POST.get("apellidos"),
                "rut": request.POST.get("rut"),
                "direccion": request.POST.get("direccion"),
                "telefono": request.POST.get("telefono"),
                "grado": request.POST.get("grado"),
            }
            update_usuario(usuario_id, data)  # Llama a la API para guardar los cambios
            return redirect("director_dashboard")
        return render(request, "editar_alumno.html", {"usuario": usuario})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


def editar_profesor(request, usuario_id):
    try:
        # Obtén los datos del profesor desde la API
        usuario = get_usuario(usuario_id)
        if request.method == "POST":
            # Procesa los datos enviados desde el formulario
            data = {
                "nombres": request.POST.get("nombres"),
                "apellidos": request.POST.get("apellidos"),
                "rut": request.POST.get("rut"),
                "direccion": request.POST.get("direccion"),
                "telefono": request.POST.get("telefono"),
                "especialidad": request.POST.get("especialidad"),
            }
            update_usuario(usuario_id, data)  # Llama a la API para actualizar los datos
            return redirect("director_dashboard")
        return render(request, "editar_profesor.html", {"usuario": usuario})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})

    return render(request, "editar_profesor.html", {"form": form, "usuario": usuario})


def inicio_view(request):
    return render(request, "inicio.html")


def usuarios_list(request):
    try:
        usuarios = get_usuarios()
        return render(request, "usuarios_list.html", {"usuarios": usuarios})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


def usuario_create(request):
    if request.method == "POST":
        data = {
            "username": request.POST["username"],
            "password": request.POST["password"],
            "role": request.POST["role"],
            "nombres": request.POST["nombres"],
            "apellidos": request.POST["apellidos"],
        }
        try:
            create_usuario(data)
            return redirect("usuarios_list")
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})
    return render(request, "usuario_form.html")


def usuario_delete(request, usuario_id):
    try:
        delete_usuario(usuario_id)
        return redirect("usuarios_list")
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})
