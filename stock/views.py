from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# importation pour methode de la fiche de stock
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import *
from .serializers import *

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

class UniteViewSet(viewsets.ModelViewSet):
    queryset = Unite.objects.all()
    serializer_class = UniteSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# class StockEntryViewSet(viewsets.ModelViewSet):
#     queryset = StockEntry.objects.all()
#     serializer_class = StockEntrySerializer

# class StockMovementViewSet(viewsets.ModelViewSet):
#     queryset = StockMovement.objects.all()
#     serializer_class = StockMovementSerializer

#     @action(detail=False, methods=['post'])
#     def retirer_stock(self, request):
#         """Retirer du stock en respectant la méthode FIFO"""
#         article_id = request.data.get('article')
#         quantite_a_retirer = int(request.data.get('quantite'))

#         try:
#             article = Article.objects.get(id=article_id)
#         except Article.DoesNotExist:
#             return Response({'error': 'Article non trouvé'}, status=status.HTTP_404_NOT_FOUND)

#         stock_entries = StockEntry.objects.filter(article=article).order_by('date_entree')  # FIFO

#         stock_restante = quantite_a_retirer
#         mouvements_effectues = []

#         for entry in stock_entries:
#             if stock_restante <= 0:
#                 break
            
#             if entry.quantite <= stock_restante:
#                 stock_restante -= entry.quantite
#                 mouvements_effectues.append(f"{entry.quantite} unités retirées de l'entrée {entry.id}")
#                 entry.delete()  # Supprime cette entrée si tout a été pris
#             else:
#                 entry.quantite -= stock_restante
#                 mouvements_effectues.append(f"{stock_restante} unités retirées de l'entrée {entry.id}")
#                 entry.save()
#                 stock_restante = 0
        
#         if stock_restante > 0:
#             return Response({'error': 'Stock insuffisant'}, status=status.HTTP_400_BAD_REQUEST)

#         # Enregistrer le mouvement
#         StockMovement.objects.create(article=article, quantite=quantite_a_retirer, date_sortie=now())

#         return Response({'message': 'Stock retiré avec succès', 'mouvements': mouvements_effectues})


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    # Ajouter une entrée de stock
    @action(detail=False, methods=['post'])
    def ajouter_entree(self, request):
        """Ajouter une entrée de stock"""
        article_id = request.data.get('article')
        quantite_ajoutee = int(request.data.get('quantite'))

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Enregistrer le mouvement d'entrée
        StockMovement.objects.create(
            article=article, quantite=quantite_ajoutee, type_mouvement='ENTREE'
        )

        return Response({'message': 'Entrée de stock ajoutée avec succès'})

    # Modifier une entrée de stock
    @action(detail=True, methods=['put'])
    def modifier_entree(self, request, pk=None):
        """Modifier un mouvement d'entrée"""
        try:
            movement = StockMovement.objects.get(id=pk, type_mouvement='ENTREE')
        except StockMovement.DoesNotExist:
            return Response({'error': 'Mouvement d\'entrée non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Mise à jour de la quantité
        quantite = request.data.get('quantite')
        if quantite is not None:
            movement.quantite = int(quantite)
            movement.save()

        return Response({'message': 'Mouvement d\'entrée modifié avec succès'})

    # Supprimer une entrée de stock
    @action(detail=True, methods=['delete'])
    def supprimer_entree(self, request, pk=None):
        """Supprimer un mouvement d'entrée"""
        try:
            movement = StockMovement.objects.get(id=pk, type_mouvement='ENTREE')
        except StockMovement.DoesNotExist:
            return Response({'error': 'Mouvement d\'entrée non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Supprimer l'entrée de stock
        movement.delete()

        return Response({'message': 'Mouvement d\'entrée supprimé avec succès'})

    # Retirer du stock (méthode FIFO)
    @action(detail=False, methods=['post'])
    def retirer_stock(self, request):
        """Retirer du stock en respectant la méthode FIFO"""
        article_id = request.data.get('article')
        quantite_a_retirer = int(request.data.get('quantite'))

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer tous les mouvements d'entrée pour cet article (FIFO)
        stock_entries = StockMovement.objects.filter(
            article=article, type_mouvement='ENTREE'
        ).order_by('date_mouvement')  # Tri pour respecter FIFO

        stock_restante = quantite_a_retirer
        mouvements_effectues = []

        for entry in stock_entries:
            if stock_restante <= 0:
                break
            
            if entry.quantite <= stock_restante:
                stock_restante -= entry.quantite
                mouvements_effectues.append(f"{entry.quantite} unités retirées de l'entrée {entry.id}")
                entry.delete()  # Supprimer cette entrée si tout a été pris
            else:
                entry.quantite -= stock_restante
                mouvements_effectues.append(f"{stock_restante} unités retirées de l'entrée {entry.id}")
                entry.save()
                stock_restante = 0
        
        if stock_restante > 0:
            return Response({'error': 'Stock insuffisant'}, status=status.HTTP_400_BAD_REQUEST)

        # Enregistrer le mouvement de sortie
        StockMovement.objects.create(
            article=article, quantite=quantite_a_retirer, type_mouvement='SORTIE'
        )

        return Response({'message': 'Stock retiré avec succès', 'mouvements': mouvements_effectues})

    # Modifier un mouvement de sortie
    @action(detail=True, methods=['put'])
    def modifier_sortie(self, request, pk=None):
        """Modifier un mouvement de sortie"""
        try:
            movement = StockMovement.objects.get(id=pk, type_mouvement='SORTIE')
        except StockMovement.DoesNotExist:
            return Response({'error': 'Mouvement de sortie non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
        # Mise à jour de la quantité
        quantite = request.data.get('quantite')
        if quantite is not None:
            movement.quantite = int(quantite)
            movement.save()

            # Réajustement du stock en fonction du FIFO
            article = movement.article
            stock_entries = StockMovement.objects.filter(article=article, type_mouvement='ENTREE').order_by('date_mouvement')
            stock_restante = movement.quantite
            mouvements_effectues = []

            for entry in stock_entries:
                if stock_restante <= 0:
                    break
                
                if entry.quantite <= stock_restante:
                    stock_restante -= entry.quantite
                    mouvements_effectues.append(f"{entry.quantite} unités retirées de l'entrée {entry.id}")
                    entry.delete()
                else:
                    entry.quantite -= stock_restante
                    mouvements_effectues.append(f"{stock_restante} unités retirées de l'entrée {entry.id}")
                    entry.save()
                    stock_restante = 0
            
            return Response({'message': 'Mouvement modifié avec succès', 'mouvements': mouvements_effectues})

        return Response({'error': 'Quantité non spécifiée'}, status=status.HTTP_400_BAD_REQUEST)

    # Supprimer un mouvement de sortie
    @action(detail=True, methods=['delete'])
    def supprimer_sortie(self, request, pk=None):
        """Supprimer un mouvement de sortie"""
        try:
            movement = StockMovement.objects.get(id=pk, type_mouvement='SORTIE')
        except StockMovement.DoesNotExist:
            return Response({'error': 'Mouvement de sortie non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Réintégrer le stock retiré
        article = movement.article
        stock_entries = StockMovement.objects.filter(article=article, type_mouvement='ENTREE').order_by('date_mouvement')
        stock_restante = movement.quantite
        mouvements_effectues = []

        for entry in stock_entries:
            if stock_restante <= 0:
                break
            
            if entry.quantite <= stock_restante:
                stock_restante -= entry.quantite
                mouvements_effectues.append(f"{entry.quantite} unités réintégrées de l'entrée {entry.id}")
                entry.delete()
            else:
                entry.quantite -= stock_restante
                mouvements_effectues.append(f"{stock_restante} unités réintégrées de l'entrée {entry.id}")
                entry.save()
                stock_restante = 0

        # Supprimer le mouvement de sortie
        movement.delete()

        return Response({'message': 'Mouvement supprimé et stock réintégré', 'mouvements': mouvements_effectues})
    

# fiche de stock
@api_view(['GET'])
def fiche_stock(request, article_id):
    """
    Génère la fiche de stock pour un article donné.
    La fiche liste tous les mouvements de stock triés par date et calcule le stock restant après chaque mouvement.
    """
    article = get_object_or_404(Article, id=article_id)
    
    # Récupérer tous les mouvements de stock pour l'article, triés par date
    mouvements = StockMovement.objects.filter(article=article).order_by('date_mouvement')
    
    stock_actuel = 0
    fiche = []
    
    # Pour chaque mouvement, mettre à jour le stock et enregistrer l'évolution
    for mouvement in mouvements:
        if mouvement.type_mouvement == 'ENTREE':
            stock_actuel += mouvement.quantite
        elif mouvement.type_mouvement == 'SORTIE':
            stock_actuel -= mouvement.quantite
        
        fiche.append({
            'date': mouvement.date_mouvement,
            'type': mouvement.type_mouvement,
            'quantite': mouvement.quantite,
            'stock_restant': stock_actuel
        })
    
    return Response({
        'article': article.nom,
        'stock_final': stock_actuel,
        'mouvements': fiche
    })

# Génération de la fiche de stock au format PDF
@api_view(['GET'])
def fiche_stock_pdf(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    mouvements = StockMovement.objects.filter(article=article).order_by('date_mouvement')
    
    stock_actuel = 0
    fiche = []
    for mouvement in mouvements:
        if mouvement.type_mouvement == 'ENTREE':
            stock_actuel += mouvement.quantite
        elif mouvement.type_mouvement == 'SORTIE':
            stock_actuel -= mouvement.quantite
        fiche.append({
            'date': mouvement.date_mouvement,
            'type': mouvement.type_mouvement,
            'quantite': mouvement.quantite,
            'stock_restant': stock_actuel
        })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fiche_stock_{article.nom}.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, f"Fiche de Stock: {article.nom}")
    y -= 40
    p.setFont("Helvetica", 12)
    p.drawString(30, y, "Date")
    p.drawString(150, y, "Mouvement")
    p.drawString(250, y, "Quantité")
    p.drawString(350, y, "Stock Restant")
    y -= 20

    for item in fiche:
        p.drawString(30, y, str(item['date'])[:19])
        p.drawString(150, y, item['type'])
        p.drawString(250, y, str(item['quantite']))
        p.drawString(350, y, str(item['stock_restant']))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    
    return response