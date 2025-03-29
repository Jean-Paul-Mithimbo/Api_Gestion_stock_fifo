from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, StockEntryViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'stock-entries', StockEntryViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
