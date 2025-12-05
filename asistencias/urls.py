from django.urls import path
from .views import AsistenciasAPIView

urlpatterns = [
    path("", AsistenciasAPIView.as_view(), name="asistencias"),
]