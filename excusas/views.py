from rest_framework import viewsets, permissions
from .models import Excusa
from .serializers import ExcusaSerializer

class ExcusaViewSet(viewsets.ModelViewSet):
    queryset = Excusa.objects.all().order_by('-fecha_presentacion')
    serializer_class = ExcusaSerializer
    permission_classes = [permissions.AllowAny]
