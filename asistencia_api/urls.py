from rest_framework.routers import DefaultRouter
from .views import FaltaViewSet, ExcusaViewSet

router = DefaultRouter()
router.register(r'faltas', FaltaViewSet)
router.register(r'excusas', ExcusaViewSet)

urlpatterns = router.urls