from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Regla
from .serializers import ReglaSerializer


class ReglamentoAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        reglamentos = Regla.objects.all().order_by('-id')
        serializer = ReglaSerializer(reglamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReglaSerializer(data=request.data)
        if serializer.is_valid():
            regla = serializer.save()
            return Response(ReglaSerializer(regla).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
