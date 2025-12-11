from django.db import models

class Practica(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, default='')
    password = models.CharField(max_length=128)
    


    def __str__(self):
        return self.username


class Obra(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    personajes = models.CharField(max_length=500, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    etiquetas = models.CharField(max_length=500, blank=True)
    imagen = models.ImageField(upload_to='obras/', null=True, blank=True)
    imagen_url = models.CharField(max_length=500, blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(Practica, on_delete=models.CASCADE)

class Capitulo(models.Model):
    titulo = models.CharField(max_length=200, default="Sin Titulo")
    contenido = models.TextField(blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

