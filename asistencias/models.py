from django.db import models
from django.conf import settings

class Asistencia(models.Model):
    aprendiz = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, default="presente")

    def __str__(self):
        return f"Asistencia {self.fecha} - {self.aprendiz}"
