from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer, AprendizSerializer

class UsuariosAPIView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

class AprendicesAPIView(APIView):
    def get(self, request):
        aprendices = Usuario.objects.filter(rol='aprendiz')
        serializer = AprendizSerializer(aprendices, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AprendizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        return Response({"message": "Login correcto"})

class PerfilAPIView(APIView):
    def get(self, request):
        return Response({"perfil": "datos del usuario"})
