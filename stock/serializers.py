from rest_framework import serializers
from .models import Article, StockEntry, StockMovement

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

