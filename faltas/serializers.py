from rest_framework import serializers
from .models import Falta

class FaltaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Falta
        fields = '__all__'
        read_only_fields = ('fecha_limite_excusa','created_at')
