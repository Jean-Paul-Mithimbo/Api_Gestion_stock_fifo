# from django.db import models

# class Categorie(models.Model):
#     libele=models.CharField(max_length=100)
#     description=models.TextField(blank=True,null=True)

#     def __str__(self):
#         return f"forme {self.libele}"
# class Forme(models.Model):
#     libele=models.CharField(max_length=100)
#     description=models.TextField(blank=True,null=True)

#     def __str__(self):
#         return f"forme {self.libele}"

# class Couleur(models.Model):
#     libele=models.CharField(max_length=100)
#     description=models.TextField(blank=True,null=True)
#     def __str__(self):
#         return f"couleur {self.libele}"


# class Type(models.Model):
#     libele=models.CharField(max_length=100)
#     description=models.TextField(blank=True,null=True)
#     def __str__(self):
#         return f"Type  {self.libele}"

# class Article(models.Model):
#     nom = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True, null=True)
#     categorie = models.ForeignKey(Categorie,related_name="categorie_article",on_delete=models.CASCADE)
#     type = models.ForeignKey(Type,null=True,on_delete=models.CASCADE)
#     forme = models.ForeignKey(Forme,null=True, on_delete=models.CASCADE,related_name="forme_article")
#     couleur = models.ForeignKey(Couleur,on_delete=models.CASCADE, related_name="couleur_Article")
#     prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
#     prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
#     seuil_reapprovisionnement = models.PositiveIntegerField(default=10)

#     def stock_total(self):
#         return sum(entry.quantite for entry in self.stock_entries.all())

#     def __str__(self):
#         return f"{self.nom} ({self.stock_total()} en stock)"

# class StockEntry(models.Model):
#     article = models.ForeignKey(Article, related_name="stock_entries", on_delete=models.CASCADE)
#     quantite = models.PositiveIntegerField()
#     date_entree = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.article.nom} - {self.quantite} unités entrées le {self.date_entree}"

# class StockMovement(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     quantite = models.PositiveIntegerField()
#     date_sortie = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.article.nom} - {self.quantite} unités sorties le {self.date_sortie}"


from django.db import models

class Categorie(models.Model):
    libele = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libele

class Forme(models.Model):
    libele = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libele

class Couleur(models.Model):
    libele = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libele

class Type(models.Model):
    libele = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libele
    
class Unite(models.Model):
    libele = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.libele

class Article(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)
    forme = models.ForeignKey(Forme, null=True, on_delete=models.CASCADE)
    couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE)
    seuil_reapprovisionnement = models.PositiveIntegerField(default=10)
    unite = models.ForeignKey(Unite, null=True, on_delete=models.CASCADE)

    def stock_total(self):
        return sum(entry.quantite for entry in self.stock_entries.all())

    def __str__(self):
        return f"{self.nom}"

class StockMovement(models.Model):
    MOUVEMENT_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="mouvements_stock")
    quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    type_mouvement = models.CharField(max_length=10, choices=MOUVEMENT_CHOICES)

    def __str__(self):
        return f"{self.article.nom} - {self.quantite} unités ({self.type_mouvement})"
