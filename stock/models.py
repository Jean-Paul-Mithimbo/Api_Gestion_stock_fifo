from django.db import models

class Article(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    categorie = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    forme = models.CharField(max_length=100, blank=True, null=True)
    couleur = models.CharField(max_length=100, blank=True, null=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    seuil_reapprovisionnement = models.PositiveIntegerField(default=10)

    def stock_total(self):
        return sum(entry.quantite for entry in self.stock_entries.all())

    def __str__(self):
        return f"{self.nom} ({self.stock_total()} en stock)"

class StockEntry(models.Model):
    article = models.ForeignKey(Article, related_name="stock_entries", on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_entree = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.nom} - {self.quantite} unités entrées le {self.date_entree}"

class StockMovement(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_sortie = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.nom} - {self.quantite} unités sorties le {self.date_sortie}"
