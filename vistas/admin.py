from django.contrib import admin

from .models import Practica, Obra, Capitulo

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")  # Agregado email y password
    search_fields = ("username", "email")
    list_filter = ("username",)

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "autor", "categoria")
    search_fields = ("titulo", "autor__username")

@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "obra", "fecha_creacion")
    search_fields = ("titulo", "obra__titulo")