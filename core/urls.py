from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Rutas para el Alumno
    path('alumno/', views.alumno_dashboard, name='alumno_dashboard'),

    # Rutas para el Profesor
    path('profesor/', views.profesor_dashboard, name='profesor_dashboard'),
    path('profesor/agregar-nota/', views.agregar_nota, name='agregar_nota'),
    path('profesor/editar-nota/<str:nota_id>/', views.editar_nota, name='editar_nota'),
    path('profesor/eliminar-nota/<str:nota_id>/', views.eliminar_nota, name='eliminar_nota'),

    # Rutas para el Director
    path('director/', views.director_dashboard, name='director_dashboard'),
    path('director/agregar-asignatura/', views.agregar_asignatura, name='agregar_asignatura'),
    path('director/editar-asignatura/<str:asignatura_id>/', views.editar_asignatura, name='editar_asignatura'),
    path('director/eliminar-asignatura/<str:asignatura_id>/', views.eliminar_asignatura, name='eliminar_asignatura'),
    path('director/agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('director/eliminar-usuario/<str:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Rutas genéricas para editar usuarios
    path('director/editar-usuario/<str:usuario_id>/<str:role>/', views.editar_usuario, name='editar_usuario'),
]
