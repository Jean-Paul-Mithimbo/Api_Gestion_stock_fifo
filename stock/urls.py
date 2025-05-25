from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, FormeViewSet, CouleurViewSet, TypeViewSet,ArticleViewSet,UniteViewSet,StockViewSet,EntreeViewSet,SortieViewSet
from .views import fiche_stock_article_pdf,bon_entree_pdf,bon_sortie_pdf, facture_sortie_pdf,fiche_inventaire_pdf

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
    path('bon-entree/<int:entree_id>/', bon_entree_pdf, name='bon_entree_pdf'),
    path('bon-sortie/<int:sortie_id>/', bon_sortie_pdf, name='bon_sortie_pdf'),
    path('facture-sortie/<int:sortie_id>/', facture_sortie_pdf, name='facture_sortie_pdf'),
    path('fiche-inventaire/', fiche_inventaire_pdf, name='fiche_inventaire_pdf'),

]
