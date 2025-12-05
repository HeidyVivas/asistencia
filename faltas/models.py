# Create your models here.
from django.db import models
from django.conf import settings
from datetime import date, timedelta
from reglamento.models import Regla

User = settings.AUTH_USER_MODEL

def sumar_dias_habiles(fecha_inicio: date, dias: int):
    actual = fecha_inicio
    añadidos = 0
    while añadidos < dias:
        actual += timedelta(days=1)
        if actual.weekday() < 5:
            añadidos += 1
    return actual

class Falta(models.Model):
    aprendiz = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faltas')
    fecha_falta = models.DateField()
    es_tardanza = models.BooleanField(default=False)
    fecha_limite_excusa = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=(
        ('pendiente','Pendiente'),
        ('excusada','Excusada'),
        ('no_valida','No válida'),
        ('vencida','Vencida')
    ), default='pendiente')
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='faltas_creadas')
    created_at = models.DateTimeField(auto_now_add=True)

    def calcular_limite(self):
        regla = Regla.objects.order_by('-id').first()
        dias = regla.dias_habiles_para_excusa if regla else 3
        fecha_inicio = self.fecha_falta
        # Aceptar strings en formato ISO (YYYY-MM-DD) cuando la instancia aún no
        # ha sido convertida por el campo DateField (ej. al crear por ORM con string)
        if isinstance(fecha_inicio, str):
            try:
                fecha_inicio = date.fromisoformat(fecha_inicio)
            except Exception:
                # Si falla el parseo, fallback a la fecha de hoy
                fecha_inicio = date.today()
        return sumar_dias_habiles(fecha_inicio, dias)

    def save(self, *args, **kwargs):
        if not self.fecha_limite_excusa:
            self.fecha_limite_excusa = self.calcular_limite()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Falta {self.aprendiz} - {self.fecha_falta} ({self.estado})"
