from django.db import models

class Regla(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    dias_habiles_para_excusa = models.IntegerField(default=3)
    tipos_documento_permitidos = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.nombre
