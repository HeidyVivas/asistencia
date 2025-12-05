# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    rol = models.CharField(max_length=20, choices=[
        ('instructor', 'Instructor'),
        ('aprendiz', 'Aprendiz'),
    ])
