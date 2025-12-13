from django.urls import path
from . import views

# ==============================================================================
# Rutas de la Aplicación 'vistas'
# ==============================================================================

urlpatterns = [
    # --------------------------------------------------
    # Páginas Públicas
    # --------------------------------------------------
    path('', views.inicio, name="inicio"),                 # Landing page
    path('buscar/', views.buscar, name="buscar"),          # Buscador global
    path('ver_obra/<int:obra_id>/', views.ver_obra, name="ver_obra"), # Detalle de obra

    # --------------------------------------------------
    # Autenticación y Perfil
    # --------------------------------------------------
    path('formulario/', views.formulario, name="formulario"), # Registro
    path('login/', views.login, name="login"),                # Inicio de sesión
    path('dashboard/', views.dashboard, name="dashboard"),    # Home privado
    path('perfil/', views.perfil, name="perfil"),             # Perfil de usuario

    # --------------------------------------------------
    # Gestión de Obras (Crear/Editar)
    # --------------------------------------------------
    path('publicar/', views.publicar, name="publicar"),
    path('editar_obra/<int:obra_id>/', views.editar_obra, name="editar_obra"),
    path('eliminar_obra/<int:obra_id>/', views.eliminar_obra, name="eliminar_obra"),

    # --------------------------------------------------
    # Gestión de Capítulos (Escribir/Editar)
    # --------------------------------------------------
    path('escribir_contenido/', views.escribir_contenido, name="escribir_contenido"), # Primer capítulo
    path('tabla_contenidos/<int:obra_id>/', views.tabla_contenidos, name="tabla_contenidos"),
    path('escribir_capitulo/<int:obra_id>/', views.escribir_capitulo, name="escribir_capitulo_nuevo"),
    path('escribir_capitulo/<int:obra_id>/<int:capitulo_id>/', views.escribir_capitulo, name="escribir_capitulo"),
    path('eliminar_capitulo/<int:capitulo_id>/', views.eliminar_capitulo, name="eliminar_capitulo"),

    # --------------------------------------------------
    # Lectura
    # --------------------------------------------------
    path('leer/<int:obra_id>/', views.leer_capitulo, name="leer_capitulo_inicio"),
    path('leer/<int:obra_id>/<int:capitulo_id>/', views.leer_capitulo, name="leer_capitulo"),

    # --------------------------------------------------
    # Administración de Usuarios
    # --------------------------------------------------
    path('usuarios/', views.lista_usuarios, name="lista_usuarios"),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name="eliminar_usuario"),
    path('editar/<int:usuario_id>/', views.editar_usuario, name="editar_usuario"),
]
