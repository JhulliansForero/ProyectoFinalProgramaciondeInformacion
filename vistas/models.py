from django.db import models

class Practica(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, default='')
    password = models.CharField(max_length=128)
    


    def __str__(self):
        return self.username

