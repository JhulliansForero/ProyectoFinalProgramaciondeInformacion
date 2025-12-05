from django.urls import path
from . import views
urlpatterns = [
    path("saludo/", views.saludo),
    path("petro/", views.petro, name="principal"),
    path("uribe/", views.uribe, name="secundario"),
    path('formulario/', views.formulario, name="formulario"),
    path('login/', views.login, name="login"),
    path('usuarios/', views.lista_usuarios, name="lista_usuarios"),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name="eliminar_usuario"),
    path('editar/<int:usuario_id>/', views.editar_usuario, name="editar_usuario"),
]
