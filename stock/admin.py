from django.contrib import admin
from .models import Article, StockEntry, StockMovement,Categorie,Forme,Couleur,Type

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('libele', 'description')
    search_fields = ('libele')
    list_filter = ('libele')

@admin.register(Forme)
class FormeAdmin(admin.ModelAdmin):
    list_display = ('libele', 'description')
    search_fields = ('libele')
    list_filter = ('libele')

@admin.register(Couleur)
class CouleurAdmin(admin.ModelAdmin):
    list_display = ('libele', 'description')
    search_fields = ('libele')
    list_filter = ('libele')

@admin.register(Type)
class CouleurAdmin(admin.ModelAdmin):
    list_display = ('libele', 'description')
    search_fields = ('libele')
    list_filter = ('libele')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix_achat', 'prix_vente', 'stock_total', 'seuil_reapprovisionnement')
    search_fields = ('nom', 'categorie', 'type', 'forme', 'couleur')
    list_filter = ('categorie', 'type', 'forme', 'couleur')

@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ('article', 'quantite', 'date_entree')
    search_fields = ('article__nom',)
    list_filter = ('date_entree',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('article', 'quantite', 'date_sortie')
    search_fields = ('article__nom',)
    list_filter = ('date_sortie',)
