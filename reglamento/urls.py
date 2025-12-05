from django.urls import path
from .views import ReglamentoAPIView

urlpatterns = [
    path("", ReglamentoAPIView.as_view(), name="reglamento"),
]