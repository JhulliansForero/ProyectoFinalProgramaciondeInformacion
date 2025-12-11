from django.urls import path
from . import views
urlpatterns = [
    path('', views.inicio, name="inicio"),  # Página principal
    path("saludo/", views.saludo),
    path("petro/", views.petro, name="principal"),
    path("uribe/", views.uribe, name="secundario"),
    path('formulario/', views.formulario, name="formulario"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),  # Vista privada
    path('perfil/', views.perfil, name="perfil"),  # Vista de perfil
    path('usuarios/', views.lista_usuarios, name="lista_usuarios"),
    
    
    # Esta ruta recibe un ID de usuario en la URL (ejemplo: /eliminar/5/)
    # El <int:usuario_id> captura el número y lo pasa a la función como parámetro
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name="eliminar_usuario"),
    
    path('editar/<int:usuario_id>/', views.editar_usuario, name="editar_usuario"),
]
