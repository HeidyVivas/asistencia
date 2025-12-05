from rest_framework import serializers
from .models import Falta, Excusa

class FaltaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Falta
        fields = '__all__'

class ExcusaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excusa
        fields = '__all__'