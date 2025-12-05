from django.urls import path, include
from rest_framework import routers
from .views import FaltaViewSet

router = routers.DefaultRouter()
router.register(r'', FaltaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
