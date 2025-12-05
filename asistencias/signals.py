from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Asistencia
from faltas.models import Falta


@receiver(post_save, sender=Asistencia)
def crear_falta_si_falto(sender, instance, created, **kwargs):
    if instance.estado == 'falto':
        falta, created_falta = Falta.objects.get_or_create(
            aprendiz=instance.aprendiz,
            fecha_falta=instance.llamada.fecha,
            defaults={'es_tardanza': False, 'creada_por': instance.llamada.instructor}
        )
        # crear notificación
