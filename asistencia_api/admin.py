from django.contrib import admin
from .models import Falta, Excusa
from django.utils import timezone
from django.core.exceptions import ValidationError

@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    list_display = ('aprendiz', 'fecha_falta', 'es_tardanza', 'fecha_limite_excusa')
    list_filter = ('es_tardanza', 'fecha_falta')
    search_fields = ('aprendiz__username',)
    ordering = ('-fecha_falta',)
    
    fieldsets = (
        ('Información del Aprendiz', {
            'fields': ('aprendiz',)
        }),
        ('Detalles de la Falta', {
            'fields': ('fecha_falta', 'es_tardanza', 'fecha_limite_excusa')
        }),
    )
    
    readonly_fields = ('fecha_limite_excusa',)

    def save_model(self, request, obj, form, change):
        hoy = timezone.now().date()
        
        # Validar que la fecha no sea en el futuro
        if obj.fecha_falta > hoy:
            raise ValidationError(f'❌ No se puede registrar una falta en una fecha futura.\nFecha ingresada: {obj.fecha_falta}\nHoy: {hoy}')
        
        # Validar máximo de faltas y ausencias
        existing_faltas = Falta.objects.filter(aprendiz=obj.aprendiz, es_tardanza=False)
        existing_ausencias = Falta.objects.filter(aprendiz=obj.aprendiz, es_tardanza=True)
        
        if change:  # Si es una actualización
            existing_faltas = existing_faltas.exclude(id=obj.id)
            existing_ausencias = existing_ausencias.exclude(id=obj.id)
        
        if not obj.es_tardanza and existing_faltas.count() >= 3:
            raise ValidationError(f'❌ El aprendiz "{obj.aprendiz.username}" ya tiene 3 faltas registradas.\nActualmente tiene: {existing_faltas.count()} faltas')
        
        if obj.es_tardanza and existing_ausencias.count() >= 3:
            raise ValidationError(f'❌ El aprendiz "{obj.aprendiz.username}" ya tiene 3 ausencias registradas.\nActualmente tiene: {existing_ausencias.count()} ausencias')
        
        super().save_model(request, obj, form, change)

@admin.register(Excusa)
class ExcusaAdmin(admin.ModelAdmin):
    list_display = ('falta', 'estado', 'fecha_presentacion')
    list_filter = ('estado', 'fecha_presentacion')
    search_fields = ('falta__aprendiz__username',)
    ordering = ('-fecha_presentacion',)
    readonly_fields = ('fecha_presentacion',)
