from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response

class AuthAPIView(APIView):
    def get(self, request):
        return Response({"message": "API de autenticación. Use /login/ o /logout/"})

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),

    path('api/usuarios/', include('usuarios.urls')),
    path('api/reglamento/', include('reglamento.urls')),
    path('api/asistencias/', include('asistencias.urls')),
    path('api/faltas/', include('faltas.urls')),
    path('api/excusas/', include('excusas.urls')),
    path('api-auth/', AuthAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
