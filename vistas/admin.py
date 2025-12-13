from django.contrib import admin
from .models import Practica, Obra, Capitulo

# ==============================================================================
# Configuración del Panel de Administración de Django
# ==============================================================================

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    """
    Administración de usuarios (Modelo Practica).
    Muestra: ID, Username, Email, Password.
    Búsqueda por: Username, Email.
    """
    list_display = ("id", "username", "email", "password")
    search_fields = ("username", "email")
    list_filter = ("username",)


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    """
    Administración de libros/obras.
    Muestra: ID, Título, Autor, Categoría.
    Búsqueda por: Título, Autor.
    """
    list_display = ("id", "titulo", "autor", "categoria")
    search_fields = ("titulo", "autor__username")


@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    """
    Administración de capítulos individuales.
    Muestra: ID, Título, Obra padre, Fecha.
    """
    list_display = ("id", "titulo", "obra", "fecha_creacion")
    search_fields = ("titulo", "obra__titulo")