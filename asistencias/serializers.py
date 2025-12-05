from rest_framework import serializers
from .models import Asistencia


class AsistenciaSerializer(serializers.ModelSerializer):
    aprendiz_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Asistencia
        fields = ['id', 'aprendiz', 'aprendiz_nombre', 'fecha', 'estado']
    
    def get_aprendiz_nombre(self, obj):
        return f"{obj.aprendiz.first_name} {obj.aprendiz.last_name}"
