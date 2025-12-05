from django.contrib import admin
from .models import Excusa

@admin.register(Excusa)
class ExcusaAdmin(admin.ModelAdmin):
    list_display = ('aprendiz','falta','tipo_documento','estado','fecha_presentacion')
    list_filter = ('estado','tipo_documento')
