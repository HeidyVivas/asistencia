from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AprendizSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, default='aprendiz123')
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        validated_data['rol'] = 'aprendiz'
        password = validated_data.pop('password', 'aprendiz123')
        instance = Usuario(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
