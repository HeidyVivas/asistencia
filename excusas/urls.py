from django.urls import path, include
from rest_framework import routers
from .views import ExcusaViewSet

router = routers.DefaultRouter()
router.register(r'', ExcusaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
