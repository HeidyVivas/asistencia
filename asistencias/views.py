from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Asistencia
from .serializers import AsistenciaSerializer
import traceback


class AsistenciasAPIView(APIView):
    def get(self, request):
        try:
            asistencias = Asistencia.objects.all()
            serializer = AsistenciaSerializer(asistencias, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            print(f"POST request data: {request.data}")
            serializer = AsistenciaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
