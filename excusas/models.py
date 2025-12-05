from django.db import models
from django.conf import settings
from faltas.models import Falta
from reglamento.models import Regla

User = settings.AUTH_USER_MODEL

class Excusa(models.Model):
    falta = models.OneToOneField(Falta, on_delete=models.CASCADE, related_name='excusa')
    aprendiz = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=100)  # ej: NOTA_MEDICA, CONSTANCIA
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='excusas/', null=True, blank=True)
    fecha_presentacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=(
        ('cargada','Cargada'),
        ('aprobada','Aprobada'),
        ('rechazada','Rechazada')
    ), default='cargada')
    razon_rechazo = models.TextField(blank=True, null=True)

    def es_valida_por_tiempo(self):
        if not self.falta.fecha_limite_excusa:
            return False
        return self.fecha_presentacion <= self.falta.fecha_limite_excusa

    def validar_segun_reglamento(self):
        regla = Regla.objects.order_by('-id').first()
        permitidos = regla.tipos_documento_permitidos if regla else []
        if self.tipo_documento not in permitidos:
            return False, f"Tipo de documento {self.tipo_documento} no permitido."
        if not self.es_valida_por_tiempo():
            return False, "La excusa fue presentada fuera del plazo."
        return True, "Excusa válida"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.estado == 'cargada':
            valido, mensaje = self.validar_segun_reglamento()
            if valido:
                self.estado = 'aprobada'
                self.razon_rechazo = ''
            else:
                self.estado = 'rechazada'
                self.razon_rechazo = mensaje
            super().save(update_fields=['estado','razon_rechazo'])

    def __str__(self):
        return f"Excusa {self.aprendiz} - {self.falta.fecha_falta} ({self.estado})"
