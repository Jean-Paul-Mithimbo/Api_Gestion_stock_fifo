from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, FormeViewSet, CouleurViewSet, TypeViewSet,ArticleViewSet, StockEntryViewSet, StockMovementViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'categories', CategorieViewSet)
router.register(r'formes', FormeViewSet)
router.register(r'couleurs', CouleurViewSet)
router.register(r'types', TypeViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'stock-entries', StockEntryViewSet)
router.register(r'stock-movements', StockMovementViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Aide aux Vulnérables API",
        default_version='v1',
        description="Documentation de l'API pour le projet Aide aux Vulnérables",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
