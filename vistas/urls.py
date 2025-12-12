from django.urls import path
from . import views
urlpatterns = [
    path('', views.inicio, name="inicio"),  # Página principal

    path('formulario/', views.formulario, name="formulario"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),  # Vista privada
    path('perfil/', views.perfil, name="perfil"),  # Vista de perfil
    path('usuarios/', views.lista_usuarios, name="lista_usuarios"),
    path('publicar/', views.publicar, name="publicar"),
    path('escribir_contenido/', views.escribir_contenido, name="escribir_contenido"),
    path('tabla_contenidos/<int:obra_id>/', views.tabla_contenidos, name="tabla_contenidos"),
    path('escribir_capitulo/<int:obra_id>/', views.escribir_capitulo, name="escribir_capitulo_nuevo"),
    path('escribir_capitulo/<int:obra_id>/<int:capitulo_id>/', views.escribir_capitulo, name="escribir_capitulo"),
    path('eliminar_capitulo/<int:capitulo_id>/', views.eliminar_capitulo, name="eliminar_capitulo"),
    path('eliminar_obra/<int:obra_id>/', views.eliminar_obra, name="eliminar_obra"),
    path('ver_obra/<int:obra_id>/', views.ver_obra, name="ver_obra"),
    path('editar_obra/<int:obra_id>/', views.editar_obra, name="editar_obra"),
    
    
    # Esta ruta recibe un ID de usuario en la URL (ejemplo: /eliminar/5/)
    # El <int:usuario_id> captura el número y lo pasa a la función como parámetro
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name="eliminar_usuario"),
    
    path('editar/<int:usuario_id>/', views.editar_usuario, name="editar_usuario"),
]
