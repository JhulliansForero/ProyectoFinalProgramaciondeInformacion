from django.contrib import admin

from .models import Practica

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")  # columnas que quieres ver
    search_fields = ("username",)                  # barra de búsqueda
    list_filter = ("username",)