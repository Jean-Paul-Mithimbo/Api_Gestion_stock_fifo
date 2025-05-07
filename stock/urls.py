from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, FormeViewSet, CouleurViewSet, TypeViewSet,ArticleViewSet,UniteViewSet,StockViewSet,EntreeViewSet,SortieViewSet
from .views import fiche_stock_article_pdf

router = DefaultRouter()
router.register(r'categories', CategorieViewSet)
router.register(r'formes', FormeViewSet)
router.register(r'couleurs', CouleurViewSet)
router.register(r'types', TypeViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'Unite', UniteViewSet)
router.register('stocks',   StockViewSet,   basename='stock')
router.register('entrees',  EntreeViewSet,  basename='entree')
router.register('sorties',  SortieViewSet,  basename='sortie')




urlpatterns = [
    path('', include(router.urls)),
    path('fiche/article/<int:article_id>/',fiche_stock_article_pdf,name='fiche-stock-article-pdf'),

]
