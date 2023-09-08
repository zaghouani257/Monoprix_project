import csv
from django.core.management.base import BaseCommand
from recapp.models import Monoprix, Carrefour, Founa

class Command(BaseCommand):
    help = 'Loads products from CSV into the database'

    def handle(self, *args, **options):
        # Load dataset1.csv
        dataset1_path = 'recapp/Updated_Datasets/dataset1.csv'
        with open(dataset1_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Monoprix.objects.create(
                    code_article=row['Code_Article'],
                    libelle_article=row['Libelle_Article'],
                    rayon=row['Rayon'],
                    famille=row['Famille'],
                    sous_famille=row['Sous famille'],
                    categorie=row['Categorie'],
                    sous_categorie=row['Sous_Categorie'],
                    prix=row['Prix'],
                    combined=row['combined'],
                    similar_product_in_carrefour=row['similar_product_in_dataset2'],
                    prix_produit_carrefour=row['Prix_Produit_dataset2'],
                    description_produit_carrefour=row['Description_Produit_dataset2'],
                    similar_product_in_founa=row['similar_product_in_dataset3'],
                    prix_produit_founa=row['Prix_Produit_dataset3'],
                    prix_produit_avant_promos_founa=row['Prix_Produit_Avant_Promos_dataset3'],
                    description_produit_founa=row['Description_Produit_dataset3']
                )

        # Load dataset2.csv
        dataset2_path = 'recapp/Updated_Datasets/dataset2.csv'
        with open(dataset2_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Carrefour.objects.create(
                    source_carrefour=row['Source_dataset2'],
                    site_carrefour=row['Site_dataset2'],
                    categorie_carrefour=row['Categorie_dataset2'],
                    lien_categorie1_carrefour=row['Lien_Categorie1_dataset2'],
                    categorie_1_carrefour=row['Categorie 1_dataset2'],
                    lien_categorie2_carrefour=row['Lien_Categorie2_dataset2'],
                    categorie_2_carrefour=row['Categorie 2_dataset2'],
                    lien_categorie3_carrefour=row['Lien_Categorie3_dataset2'],
                    categorie_3_carrefour=row['Categorie 3_dataset2'],
                    nom_produit_carrefour=row['Nom_Produit_dataset2'],
                    lien_produit_carrefour=row['Lien_Produit_dataset2'],
                    description_produit_carrefour=row['Description_Produit_dataset2'],
                    prix_produit_carrefour=row['Prix_Produit_dataset2'],
                    marque_produit_carrefour=row['Marque_Produit_dataset2'],
                    combined_dataset2=row['combined_dataset2']
                )

        # Load dataset3.csv
        dataset3_path = 'recapp/Updated_Datasets/dataset3.csv'
        with open(dataset3_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Founa.objects.create(
                    source_founa=row['Source_dataset3'],
                    site_founa=row['Site_dataset3'],
                    categorie_founa=row['Catgeorie_dataset3'],
                    lien_categorie_founa=row['Lien_Categorie_dataset3'],
                    categorie_1_founa=row['Categorie 1_dataset3'],
                    lien_categorie1_founa=row['Lien_Categorie1_dataset3'],
                    categorie_2_founa=row['Categorie 2_dataset3'],
                    categorie_3_founa=row['Categorie 3_dataset3'],
                    lien_produit_founa=row['Lien_Produit_dataset3'],
                    nom_produit_founa=row['Nom_Produit_dataset3'],
                    description_produit_founa=row['Description_Produit_dataset3'],
                    prix_produit_founa=row['Prix_Produit_dataset3'],
                    prix_produit_avant_promos_founa=row['Prix_Produit_Avant_Promos_dataset3'],
                    promo_produit_founa=row['Promo_Produit_dataset3'],
                    poids_quantite_founa=row['Poids/Quantite_dataset3'],
                    reference_produit_founa=row['Reference_Produit_dataset3'],
                    vendu_par_mg_founa=row['Vendu par MG_dataset3'],
                    combined_dataset3=row['combined_dataset3']
                )