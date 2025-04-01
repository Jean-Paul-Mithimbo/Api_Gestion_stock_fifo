from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from .models import Article, StockEntry, StockMovement,Categorie,Forme,Couleur,Type
from .serializers import ArticleSerializer, StockEntrySerializer, StockMovementSerializer,CategorieSerializer, FormeSerializer, CouleurSerializer, TypeSerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class FormeViewSet(viewsets.ModelViewSet):
    queryset = Forme.objects.all()
    serializer_class = FormeSerializer

class CouleurViewSet(viewsets.ModelViewSet):
    queryset = Couleur.objects.all()
    serializer_class = CouleurSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class StockEntryViewSet(viewsets.ModelViewSet):
    queryset = StockEntry.objects.all()
    serializer_class = StockEntrySerializer

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    @action(detail=False, methods=['post'])
    def retirer_stock(self, request):
        """Retirer du stock en respectant la méthode FIFO"""
        article_id = request.data.get('article')
        quantite_a_retirer = int(request.data.get('quantite'))

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        stock_entries = StockEntry.objects.filter(article=article).order_by('date_entree')  # FIFO

        stock_restante = quantite_a_retirer
        mouvements_effectues = []

        for entry in stock_entries:
            if stock_restante <= 0:
                break
            
            if entry.quantite <= stock_restante:
                stock_restante -= entry.quantite
                mouvements_effectues.append(f"{entry.quantite} unités retirées de l'entrée {entry.id}")
                entry.delete()  # Supprime cette entrée si tout a été pris
            else:
                entry.quantite -= stock_restante
                mouvements_effectues.append(f"{stock_restante} unités retirées de l'entrée {entry.id}")
                entry.save()
                stock_restante = 0
        
        if stock_restante > 0:
            return Response({'error': 'Stock insuffisant'}, status=status.HTTP_400_BAD_REQUEST)

        # Enregistrer le mouvement
        StockMovement.objects.create(article=article, quantite=quantite_a_retirer, date_sortie=now())

        return Response({'message': 'Stock retiré avec succès', 'mouvements': mouvements_effectues})
