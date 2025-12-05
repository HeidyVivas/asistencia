from rest_framework import viewsets, permissions
from .models import Falta
from .serializers import FaltaSerializer

class FaltaViewSet(viewsets.ModelViewSet):
    queryset = Falta.objects.all().order_by('-created_at')
    serializer_class = FaltaSerializer
    permission_classes = [permissions.AllowAny]
