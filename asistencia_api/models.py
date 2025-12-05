from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Falta(models.Model):
    aprendiz = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faltas')
    fecha_falta = models.DateField()
    es_tardanza = models.BooleanField(default=False)
    fecha_limite_excusa = models.DateField(null=True, blank=True)

    def clean(self):
        hoy = timezone.now().date()
        
        # Validar que la fecha de falta no sea en el futuro
        if self.fecha_falta > hoy:
            raise ValidationError(f'No se puede registrar una falta en una fecha futura. Fecha ingresada: {self.fecha_falta}, Hoy: {hoy}')
        
        # Al actualizar, no contar el registro actual
        existing_faltas = Falta.objects.filter(aprendiz=self.aprendiz, es_tardanza=False)
        existing_ausencias = Falta.objects.filter(aprendiz=self.aprendiz, es_tardanza=True)
        
        if self.id:  # Si es una actualización
            existing_faltas = existing_faltas.exclude(id=self.id)
            existing_ausencias = existing_ausencias.exclude(id=self.id)
        
        # Validar máximo 3 faltas por aprendiz
        if not self.es_tardanza and existing_faltas.count() >= 3:
            raise ValidationError('El aprendiz ya tiene el máximo de 3 faltas permitidas.')
        
        # Validar máximo 3 ausencias por aprendiz
        if self.es_tardanza and existing_ausencias.count() >= 3:
            raise ValidationError('El aprendiz ya tiene el máximo de 3 ausencias permitidas.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        tipo = 'Tardanza' if self.es_tardanza else 'Falta'
        return f'{tipo} de {self.aprendiz.username} en {self.fecha_falta}'

class Excusa(models.Model):
    falta = models.OneToOneField(Falta, on_delete=models.CASCADE, primary_key=True)
    fecha_presentacion = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    documento_adjunto = models.FileField(upload_to='excusas/')
    ESTADOS = [
        ('P', 'Pendiente'),
        ('A', 'Aprobada'),
        ('R', 'Rechazada'),
        ('V', 'Vencida por Plazo')
    ]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    instructor_revision = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='excusas_revisadas')

    def __str__(self):
        return f'Excusa de {self.falta.aprendiz.username} - Estado: {self.estado}'
