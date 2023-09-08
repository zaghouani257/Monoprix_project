from django.db import models

class Monoprix(models.Model):
    code_article = models.CharField(max_length=255, null=True, blank=True)
    libelle_article = models.CharField(max_length=255, null=True, blank=True)
    rayon = models.CharField(max_length=255, null=True, blank=True)
    famille = models.CharField(max_length=255, null=True, blank=True)
    sous_famille = models.CharField(max_length=255, null=True, blank=True)
    categorie = models.CharField(max_length=255, null=True, blank=True)
    sous_categorie = models.CharField(max_length=255, null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    combined = models.CharField(max_length=255, null=True, blank=True)
    similar_product_in_carrefour = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_carrefour = models.CharField(max_length=255, null=True, blank=True)
    description_produit_carrefour = models.TextField(null=True, blank=True)
    similar_product_in_founa = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_avant_promos_founa = models.CharField(max_length=255, null=True, blank=True)
    description_produit_founa = models.TextField(null=True, blank=True)

class Carrefour(models.Model):
    source_carrefour = models.CharField(max_length=255, null=True, blank=True)
    site_carrefour = models.CharField(max_length=255, null=True, blank=True)
    categorie_carrefour = models.CharField(max_length=255, null=True, blank=True)
    lien_categorie1_carrefour = models.CharField(max_length=255, null=True, blank=True)
    categorie_1_carrefour = models.CharField(max_length=255, null=True, blank=True)
    lien_categorie2_carrefour = models.CharField(max_length=255, null=True, blank=True)
    categorie_2_carrefour = models.CharField(max_length=255, null=True, blank=True)
    lien_categorie3_carrefour = models.CharField(max_length=255, null=True, blank=True)
    categorie_3_carrefour = models.CharField(max_length=255, null=True, blank=True)
    nom_produit_carrefour = models.CharField(max_length=255, null=True, blank=True)
    lien_produit_carrefour = models.CharField(max_length=255, null=True, blank=True)
    description_produit_carrefour = models.TextField(null=True, blank=True)
    prix_produit_carrefour = models.CharField(max_length=255, null=True, blank=True)
    marque_produit_carrefour = models.CharField(max_length=255, null=True, blank=True)
    combined_dataset2 = models.TextField(null=True, blank=True)

class Founa(models.Model):
    source_founa = models.CharField(max_length=255, null=True, blank=True)
    site_founa = models.CharField(max_length=255, null=True, blank=True)
    categorie_founa = models.CharField(max_length=255, null=True, blank=True)
    lien_categorie_founa = models.CharField(max_length=255, null=True, blank=True)
    categorie_1_founa = models.CharField(max_length=255, null=True, blank=True)
    lien_categorie1_founa = models.CharField(max_length=255, null=True, blank=True)
    categorie_2_founa = models.CharField(max_length=255, null=True, blank=True)
    categorie_3_founa = models.CharField(max_length=255, null=True, blank=True)
    lien_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    nom_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    description_produit_founa = models.TextField(null=True, blank=True)
    prix_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_avant_promos_founa = models.CharField(max_length=255, null=True, blank=True)
    promo_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    poids_quantite_founa = models.CharField(max_length=255, null=True, blank=True)
    reference_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    vendu_par_mg_founa = models.CharField(max_length=255, null=True, blank=True)
    combined_dataset3 = models.TextField(null=True, blank=True)

class Produit(models.Model):
    code_article = models.CharField(max_length=255, null=True, blank=True)
    similar_product_in_carrefour = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_carrefour = models.CharField(max_length=255, null=True, blank=True)
    description_produit_carrefour = models.TextField(null=True, blank=True)
    similar_product_in_founa = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_founa = models.CharField(max_length=255, null=True, blank=True)
    prix_produit_avant_promos_founa = models.CharField(max_length=255, null=True, blank=True)
    description_produit_founa = models.TextField(null=True, blank=True)