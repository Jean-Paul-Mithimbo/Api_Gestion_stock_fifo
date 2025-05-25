
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
    categorie = models.ForeignKey(Categorie,blank=True, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, null=True,blank=True, on_delete=models.CASCADE)
    forme = models.ForeignKey(Forme, null=True,blank=True, on_delete=models.CASCADE)
    couleur = models.ForeignKey(Couleur,null=True,blank=True,on_delete=models.CASCADE)
    seuil_reapprovisionnement = models.PositiveIntegerField(default=10)
    unite = models.ForeignKey(Unite, null=True, on_delete=models.CASCADE)

    # def stock_total(self):
    #     return sum(entry.quantite for entry in self.stock_entries.all())

    def __str__(self):
        return f"{self.nom}"



class Stock(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='stock')
    quantite = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.article.nom} – {self.quantite}"

class Entree(models.Model):
    libele = models.CharField(max_length=255, blank=True)
    date_op = models.DateField()

    def __str__(self):
        return f"Entrée du #{self.date_op}"

class LigneEntree(models.Model):
    entree = models.ForeignKey(Entree, related_name='lignes', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='entrees', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    date_expiration = models.DateField()
    date_entree = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite}×{self.article.nom} @ {self.prix_unitaire}"

class Sortie(models.Model):
    motif = models.CharField(max_length=255, blank=True)
    date_sor = models.DateField()

    def __str__(self):
        return f"Sortie #{self.pk}"

class LigneSortie(models.Model):
    sortie     = models.ForeignKey(Sortie, related_name='lignes', on_delete=models.CASCADE)
    article    = models.ForeignKey(Article, related_name='sorties', on_delete=models.CASCADE)
    quantite   = models.PositiveIntegerField()
    date_sortie = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite}×{self.article.nom}"
