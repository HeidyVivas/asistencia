
from django.db import models
from django.contrib.auth.models import User

class Falta(models.Model):
	aprendiz = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faltas')
	fecha_falta = models.DateField()
	es_tardanza = models.BooleanField(default=False)
	fecha_limite_excusa = models.DateField(null=True, blank=True)

	def __str__(self):
		return f'Falta de {self.aprendiz.username} en {self.fecha_falta}'

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
