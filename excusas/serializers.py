from rest_framework import serializers
from .models import Excusa

class ExcusaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excusa
        fields = '__all__'
        read_only_fields = ('fecha_presentacion',)
