from django.urls import path
from .views import UsuariosAPIView, AprendicesAPIView, LoginAPIView, PerfilAPIView

urlpatterns = [
    path("", UsuariosAPIView.as_view(), name="usuarios"),
    path("aprendices/", AprendicesAPIView.as_view(), name="aprendices"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("perfil/", PerfilAPIView.as_view(), name="perfil"),
]
