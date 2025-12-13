from django.db import models

# ==========================================
# Modelo de Usuario (Practica)
# ==========================================
class Practica(models.Model):
    """
    Modelo personalizado para manejar los usuarios de la plataforma.
    Almacena credenciales básicas y autenticación.
    """
    username = models.CharField(max_length=150, unique=True)  # Nombre de usuario único
    email = models.EmailField(max_length=150, default='')     # Correo electrónico
    password = models.CharField(max_length=128)               # Contraseña en texto plano (Nota: inseguro, mejorar a futuro)

    def __str__(self):
        return self.username


# ==========================================
# Modelo de Obra Literaria
# ==========================================
class Obra(models.Model):
    """
    Representa un libro u obra creada por un usuario.
    Contiene la metainformación del libro.
    """
    titulo = models.CharField(max_length=200)                 # Título del libro
    descripcion = models.TextField()                          # Sinopsis o resumen
    personajes = models.CharField(max_length=500, blank=True) # Lista de personajes principales
    categoria = models.CharField(max_length=100, blank=True)  # Género literario
    etiquetas = models.CharField(max_length=500, blank=True)  # Tags para búsqueda
    imagen = models.ImageField(upload_to='obras/', null=True, blank=True)       # Portada (archivo local)
    imagen_url = models.CharField(max_length=500, blank=True, null=True)        # Portada (URL externa)
    contenido = models.TextField(blank=True, null=True)       # Contenido general (opcional, vs capítulos)
    autor = models.ForeignKey(Practica, on_delete=models.CASCADE) # Relación con el autor (Usuario)

    def __str__(self):
        return self.titulo


# ==========================================
# Modelo de Capítulo
# ==========================================
class Capitulo(models.Model):
    """
    Representa un capítulo individual de una obra.
    Permite dividir el contenido en partes.
    """
    titulo = models.CharField(max_length=200, default="Sin Titulo") # Título del capítulo
    contenido = models.TextField(blank=True, null=True)             # Texto del capítulo
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)        # Relación con la Obra padre
    fecha_creacion = models.DateTimeField(auto_now_add=True)        # Fecha de publicación

    def __str__(self):
        return self.titulo
