from rest_framework.routers import DefaultRouter
from .views import FaltaViewSet, ExcusaViewSet
from django.urls import path
# from .views import dashboard

router = DefaultRouter()
router.register(r'faltas', FaltaViewSet)
router.register(r'excusas', ExcusaViewSet)

urlpatterns = router.urls

urlpatterns = [
    # path('dashboard/', dashboard, name='dashboard'),
]
