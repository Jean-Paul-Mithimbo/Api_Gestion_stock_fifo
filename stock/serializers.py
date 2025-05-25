from rest_framework import serializers
from .models import *

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class FormeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forme
        fields = '__all__'

class CouleurSerializer(serializers.ModelSerializer):
     class Meta:
        model = Couleur
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
     class Meta:
        model = Type
        fields = '__all__'
class UniteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Unite
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    stock_total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


# stock
class StockSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField()
    class Meta:
        model  = Stock
        fields = ['id', 'article', 'quantite', 'seuil_alerte']

class LigneEntreeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LigneEntree
        fields = [
            'id', 'article', 'quantite', 'prix_unitaire',
            'date_entree', 'date_expiration'
        ]

class EntreeSerializer(serializers.ModelSerializer):
    lignes = LigneEntreeSerializer(many=True)
    class Meta:
        model  = Entree
        fields = ['id', 'libele','date_op', 'lignes']

class LigneSortieSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LigneSortie
        fields = [
            'id', 'article', 'quantite', 'date_sortie'
        ]

class SortieSerializer(serializers.ModelSerializer):
    lignes = LigneSortieSerializer(many=True)
    class Meta:
        model  = Sortie
        fields = ['id', 'motif','date_sor', 'lignes']

