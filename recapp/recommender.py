import pandas as pd
from IPython.display import display
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
import os
import unicodedata
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('french'))

df = pd.read_excel('C:/Users/zagho/recproject_nouveau/recapp/Datasets/Liste Articles boissons-non-alcoolises v2023.05.xlsx')
df.to_csv('C:/Users/zagho/recproject_nouveau/recapp/Datasets/Monoprix_Boissons_non_alcoolisee.csv', index=False)

# Chargez vos datasets (remplacez les noms de fichiers par les vôtres)
dataset1 = pd.read_csv('C:/Users/zagho/recproject_nouveau/recapp/Datasets/Monoprix_Boissons_non_alcoolisee.csv')
dataset2 = pd.read_csv('C:/Users/zagho/recproject_nouveau/recapp/Datasets/Carrefour_Boissons.csv')
#dataset2 = pd.read_csv('founa_alimentation_boissons.csv')

# Remplacez les valeurs NaN par une chaîne vide pour les colonnes spécifiées
dataset1 = dataset1.fillna({"Rayon": "", "Famille": "", "Sous famille": "", "Libelle_Article": ""})
dataset2 = dataset2.fillna({"Description_Produit": "", "Marque_Produit": "", "Categorie 1": "", "Categorie 2": ""})
#dataset2 = dataset2.fillna({"Description_Produit": "", "Poids/Quantitie": "", "Categorie 1": "", "Categorie 2": ""})


# Maintenant, les chaînes vides seront utilisées pour les colonnes avec des valeurs manquantes lors de la création de la colonne "combined"
dataset1["combined"] = "Nom_Produit : " + dataset1["Libelle_Article"] + " Description_Produit : " + dataset1["Rayon"] +" Categorie 1: " + dataset1["Famille"] + " Categorie 2 : " + dataset1["Sous famille"]
dataset2["combined"] = "Nom_Produit : " + dataset2["Nom_Produit"] + " Description_Produit : " + dataset2["Description_Produit"] + " Marque_Produit : " + dataset2["Marque_Produit"]+" Categorie 1: " + dataset2["Categorie 1"] + " Categorie 2 : " + dataset2["Categorie 2"]
#dataset2["combined"] = "Nom_Produit : " + dataset2["Nom_Produit"] + " Description_Produit : " + dataset2["Description_Produit"] + " Poids/Quantite : " + dataset2["Poids/Quantite"]+" Categorie 1: " + dataset2["Categorie 1"] + " Categorie 2:  " + dataset2["Categorie 2"]

def extract_keywords(text):
    words = set(nltk.word_tokenize(text.lower()))
    return words.difference(stop_words)

# Ajoutez cette fonction pour ajuster le seuil de similarité en fonction des mots clés
def adjust_similarity_threshold(similarity, keywords1, keywords2, keyword_boost=0.1):
    common_keywords = keywords1.intersection(keywords2)
    if common_keywords:
        similarity += keyword_boost * len(common_keywords)
    return similarity
def normalize_units(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'\b(\d+(\.\d+)?)\s*ml\b', lambda m: f"{float(m.group(1)) * 1}ml", text)
        text = re.sub(r'\b(\d+(\.\d+)?)\s*cl\b', lambda m: f"{float(m.group(1)) * 10}ml", text)
        text = re.sub(r'\b(\d+(\.\d+)?)\s*g\b', lambda m: f"{float(m.group(1)) * 1}g", text)
        text = re.sub(r'\b(\d+(\.\d+)?)\s*kg\b', lambda m: f"{float(m.group(1)) * 1000}g", text)
    return text

def extract_units(text):
    units = {}
    ml_match = re.search(r'\b(\d+(\.\d+)?)\s*ml\b', text)
    if ml_match:
        units['ml'] = float(ml_match.group(1))

    g_match = re.search(r'\b(\d+(\.\d+)?)\s*g\b', text)
    if g_match:
        units['g'] = float(g_match.group(1))

    return units

def units_are_compatible(units1, units2):
    for unit in units1:
        if unit in units2:
            if abs(units1[unit] - units2[unit]) <= 1e-6:
                return True
    return False

dataset1["combined"] = dataset1["combined"].apply(normalize_units)
dataset2["combined"] = dataset2["combined"].apply(normalize_units)

model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')

dataset1_embeddings = model.encode(dataset1['combined'].tolist())
dataset2_embeddings = model.encode(dataset2['combined'].tolist())

similarity_threshold = 0.8

def find_similar_product(row):
    product1_embedding = dataset1_embeddings[row.name]
    similarity_scores = cosine_similarity([product1_embedding], dataset2_embeddings)[0]

    best_similarity_index = similarity_scores.argmax()
    best_similarity = similarity_scores[best_similarity_index]

    product1_units = extract_units(row['combined'])
    product2_units = extract_units(dataset2.loc[best_similarity_index, 'combined'])

    # Ajustez le seuil de similarité en fonction des mots clés
    product1_keywords = extract_keywords(row['Libelle_Article'])
    product2_keywords = extract_keywords(dataset2.loc[best_similarity_index, 'Nom_Produit'])
    adjusted_similarity = adjust_similarity_threshold(best_similarity, product1_keywords, product2_keywords)

    if adjusted_similarity >= similarity_threshold:
        if units_are_compatible(product1_units, product2_units):
            return pd.Series({
                "similar_product_in_dataset2": dataset2.loc[best_similarity_index, 'Nom_Produit'],
                "Prix_Produit_dataset2": dataset2.loc[best_similarity_index, 'Prix_Produit'],
                "Description_Produit_dataset2": dataset2.loc[best_similarity_index, 'Description_Produit']
            })
    
    return pd.Series({
        "similar_product_in_dataset2": None,
        "Prix_Produit_dataset2": None,
        "Description_Produit_dataset2": None
        
    })

dataset1 = dataset1.join(dataset1.apply(find_similar_product, axis=1))
display(dataset1.loc[:, ["Libelle_Article", "similar_product_in_dataset2", "Prix_Produit_dataset2", "Description_Produit_dataset2"]])
# Renommez les colonnes de dataset2 pour les distinguer de dataset1
dataset2 = dataset2.add_suffix("_dataset2")

# Fonction pour supprimer les accents des mots
def remove_accents(word):
    return ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')
# Supprimer les accents des éléments de dataset2
# Liste des colonnes à traiter
columns_to_process = ['Categorie_dataset2', 'Categorie 1_dataset2', 'Categorie 2_dataset2',
                      'Categorie 3_dataset2', 'Nom_Produit_dataset2', 'Description_Produit_dataset2',
                      'Marque_Produit_dataset2']


# Appliquer la fonction remove_accents() sur toutes les colonnes
for column in columns_to_process:
    dataset2[column] = dataset2[column].fillna("").astype(str)
    dataset2[column] = dataset2[column].apply(remove_accents)


output_folder = 'C:/Users/zagho/recproject_nouveau/recapp/Updated_Datasets'
dataset1.to_csv(output_folder + '/dataset1.csv', index=False)
dataset2.to_csv(output_folder + '/dataset2.csv', index=False)

