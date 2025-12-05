from rest_framework import serializers
from .models import Regla


class ReglaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regla
        fields = ['id', 'nombre', 'descripcion', 'dias_habiles_para_excusa', 'tipos_documento_permitidos']
