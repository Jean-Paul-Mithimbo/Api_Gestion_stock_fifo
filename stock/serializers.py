from rest_framework import serializers
from .models import Article,StockEntry,StockMouvement

class ArticleSerializer(serializers.ModelSerializer):
    stock_total=serializers.IntegerField(read_only=True)
    class Meta:
        model=Article
        fields='__all__'

class StockentrySerializer(serializers.ModelSerializer):
    class Meta:
        model=StockEntry
        fields='__all__'
        
class StockMouvementSerializer(serializers.ModelSerializer):
    class Meta:
        model=StockMouvement
        fields='__all__'

