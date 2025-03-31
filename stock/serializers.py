from rest_framework import serializers
from .models import Article, StockEntry, StockMovement,Categorie,Forme,Couleur,Type

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

class ArticleSerializer(serializers.ModelSerializer):
    stock_total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

class StockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockEntry
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'

