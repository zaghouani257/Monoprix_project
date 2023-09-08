import pandas as pd
import nltk
import spacy
import functools
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import unicodedata
import warnings
import os
import sys
from fuzzywuzzy import process

# Ajoutez le chemin du répertoire parent de recapp au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import django

# Configurez les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recproject.settings')
django.setup()

warnings.filterwarnings("ignore", category=UserWarning)

SIMILARITY_THRESHOLD = 0.1

from recapp.models import Monoprix, Carrefour, Founa


dataset1 = pd.DataFrame(list(Monoprix.objects.values()))
dataset2 = pd.DataFrame(list(Carrefour.objects.values()))
dataset3 = pd.DataFrame(list(Founa.objects.values()))

def remove_accents(word):
    return ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')

nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt', quiet=True)

from nltk.corpus import stopwords
french_stop_words = stopwords.words('french')

nlp = spacy.load("fr_core_news_md")

def correct_spelling(keyword, word_set):
    best_match = process.extractOne(keyword, word_set)
    if best_match[1] >= 80:
        return best_match[0]
    return keyword

def preprocess_tags(tags_column):
    def lemmatize(tokens):
        doc = nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]

    def filter_pos_tags(pos_tags):
        important_tags = ['NN', 'JJ', 'VB', 'NNS', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ', 'JJR', 'JJS', 'NNP', 'NNPS']
        return [word for word, tag in pos_tags if tag in important_tags]

    tags_column = tags_column.apply(lambda x: x if isinstance(x, str) else '')
    tags_column = tags_column.apply(lambda x: ''.join([c for c in x if c not in string.punctuation]))
    tags_column = tags_column.apply(lambda x: x.lower())
    tokens_column = tags_column.apply(nltk.word_tokenize)
    tokens_column = tokens_column.apply(lambda x: [w for w in x if w not in french_stop_words])
    tokens_column = tokens_column.apply(lemmatize)
    pos_tags_column = tokens_column.apply(nltk.pos_tag)
    important_tokens_column = pos_tags_column.apply(filter_pos_tags)
    final_tags_column = important_tokens_column.apply(lambda x: ' '.join(x))

    return final_tags_column

# Prepare datasets
dataset1['tags'] = preprocess_tags(dataset1['combined'])
dataset2['tags'] = preprocess_tags(dataset2['combined_dataset2'])
dataset3['tags'] = preprocess_tags(dataset3['combined_dataset3'])

# Combine the tags from all datasets
combined_tags = pd.concat([dataset1['tags'], dataset2['tags'], dataset3['tags']])

# Fit and transform the combined tags with TfidfVectorizer
tfidf = TfidfVectorizer(max_features=5000)
vectors_combined = tfidf.fit_transform(combined_tags).toarray()

# Split the combined vectors back into sets for each dataset
vectors_dataset1 = vectors_combined[:len(dataset1)]
vectors_dataset2 = vectors_combined[len(dataset1):len(dataset1)+len(dataset2)]
vectors_dataset3 = vectors_combined[len(dataset1)+len(dataset2):]

spacy_cache = {}

def spacy_similarity(w1, w2):
    key = tuple(sorted((w1, w2)))
    if key not in spacy_cache:
        spacy_cache[key] = nlp(w1).similarity(nlp(w2))
    return spacy_cache[key]

def lemmatize(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.is_alpha]

@functools.lru_cache(maxsize=None)
def lemmatize_cached(text):
    return lemmatize(text)

def name_similarity(product_name, lemmatized_keywords):
    if pd.isna(product_name) or not isinstance(product_name, str):
        return -1

    product_name = remove_accents(product_name.lower())
    name_words = product_name.split()
    max_similarity = -1

    for kw in lemmatized_keywords:
        for word in name_words:
            word = remove_accents(word)
            similarity = spacy_similarity(kw, word)
            if similarity > max_similarity:
                max_similarity = similarity

    return max_similarity

def find_most_similar(word, word_set):
    word = remove_accents(word)
    word_nlp = nlp(word)
    max_similarity = -1
    most_similar_word = None

    for w in word_set:
        w_no_accents = remove_accents(w)
        similarity = word_nlp.similarity(nlp(w_no_accents))
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_word = w

    return most_similar_word if max_similarity >= 0.6 else None
def clean_price(price_string):
    # Supprimer les symboles indésirables
    price_string = price_string.replace("\xa0", " ")
    return(price_string)
PER_PAGE_DATASET1 = 9   #12
PER_PAGE_DATASET2_AND_3 = 9
def recommend_for_row(row):
    keyword = row["keyword"]
    dataset_number = row["dataset_number"]
    page = row.get("page", 1)

    lemmatized_keywords = lemmatize_cached(keyword.lower())

    if dataset_number == 1:
        product_name_column = "libelle_article"
        vocab = set(tfidf.get_feature_names_out())
        lemmatized_keywords = [correct_spelling(w, vocab) for w in lemmatized_keywords]
        dataset = dataset1
        vectors_dataset = vectors_dataset1
    elif dataset_number == 2:
        product_name_column = "nom_produit_carrefour"
        vocab = set(tfidf.get_feature_names_out())
        lemmatized_keywords = [correct_spelling(w, vocab) for w in lemmatized_keywords]
        dataset = dataset2
        vectors_dataset = vectors_dataset2
    elif dataset_number == 3:
        product_name_column = "nom_produit_founa"
        vocab = set(tfidf.get_feature_names_out())
        lemmatized_keywords = [correct_spelling(w, vocab) for w in lemmatized_keywords]
        dataset = dataset3
        vectors_dataset = vectors_dataset3
    else:
        raise ValueError("Invalid dataset_number. It must be either 1, 2, or 3.")

    dataset["name_similarity"] = dataset[product_name_column].apply(lambda x: name_similarity(x, lemmatized_keywords))
    filtered_dataset = dataset[dataset["name_similarity"] >= 0.6]

    if filtered_dataset.empty:
        similar_word = find_most_similar(keyword, vocab)
        if similar_word is not None:
            return f"Aucun produit trouvé pour le mot-clé '{keyword}'. Essayez peut-être avec le mot-clé '{similar_word}'.", 0
        else:
            return "Aucun produit trouvé.", 0

    keyword_vector = tfidf.transform([" ".join(lemmatized_keywords)]).toarray()

    keyword_similarity = cosine_similarity(keyword_vector, vectors_dataset[filtered_dataset.index])

    keyword_similarity_with_weight = []

    for index, similarity in enumerate(keyword_similarity[0]):
        product_name = filtered_dataset.iloc[index][product_name_column]
        name_similarity_value = filtered_dataset.iloc[index]["name_similarity"]
        weighted_similarity = similarity + (0.2 * name_similarity_value)
        keyword_similarity_with_weight.append(weighted_similarity)

    sorted_indices = sorted(range(len(keyword_similarity_with_weight)), key=lambda i: keyword_similarity_with_weight[i], reverse=True)
    total_pages = (len(sorted_indices) + PER_PAGE_DATASET1 - 1) // PER_PAGE_DATASET1  # Pour dataset1
    if dataset_number == 2 or dataset_number == 3:
        total_pages = (len(sorted_indices) + PER_PAGE_DATASET2_AND_3 - 1) // PER_PAGE_DATASET2_AND_3  # Pour dataset2 et dataset3


    if dataset_number == 1:
        start = (page - 1) * PER_PAGE_DATASET1
        end = start + PER_PAGE_DATASET1
        top_products = sorted_indices[start:end]
    elif dataset_number == 2 or dataset_number == 3:
        start = (page - 1) * PER_PAGE_DATASET2_AND_3
        end = start + PER_PAGE_DATASET2_AND_3
        top_products = sorted_indices[start:end]

    if not top_products or keyword_similarity_with_weight[top_products[0]] < SIMILARITY_THRESHOLD:
        return "Ce produit n'existe pas.", total_pages

    if dataset_number == 1:
        return [(filtered_dataset.iloc[index]['id'], filtered_dataset.iloc[index][product_name_column] if pd.notnull(filtered_dataset.iloc[index][product_name_column]) else "", filtered_dataset.iloc[index]['libelle_article'] if pd.notnull(filtered_dataset.iloc[index]['libelle_article']) else "", filtered_dataset.iloc[index]['prix'] if pd.notnull(filtered_dataset.iloc[index]['prix']) else 0) for index in top_products], total_pages
    elif dataset_number == 2:
        return [(filtered_dataset.iloc[index]['id'], filtered_dataset.iloc[index][product_name_column] if pd.notnull(filtered_dataset.iloc[index][product_name_column]) else "", filtered_dataset.iloc[index]['description_produit_carrefour'] if pd.notnull(filtered_dataset.iloc[index]['description_produit_carrefour']) else "", filtered_dataset.iloc[index]['prix_produit_carrefour'] if pd.notnull(filtered_dataset.iloc[index]['prix_produit_carrefour']) else 0, filtered_dataset.iloc[index]['marque_produit_carrefour'] if pd.notnull(filtered_dataset.iloc[index]['marque_produit_carrefour']) else "") for index in top_products], total_pages
    elif dataset_number == 3:
        return [(filtered_dataset.iloc[index]['id'], filtered_dataset.iloc[index][product_name_column] if pd.notnull(filtered_dataset.iloc[index][product_name_column]) else "", filtered_dataset.iloc[index]['description_produit_founa'] if pd.notnull(filtered_dataset.iloc[index]['description_produit_founa']) else "", clean_price(filtered_dataset.iloc[index]['prix_produit_founa']) if pd.notnull(clean_price(filtered_dataset.iloc[index]['prix_produit_founa'])) else 0, clean_price(filtered_dataset.iloc[index]['prix_produit_avant_promos_founa']) if pd.notnull(clean_price(filtered_dataset.iloc[index]['prix_produit_avant_promos_founa'])) else 0) for index in top_products], total_pages
    else:
        raise ValueError("Invalid dataset_number. It must be either 1, 2, or 3.")

# Test the function with a DataFrame
test_data = pd.DataFrame({"keyword": ["boisson", "boisson"], "dataset_number": [1, 2]})
test_data["results"] = test_data.apply(recommend_for_row, axis=1)

result1 = recommend_for_row({"keyword": "eau", "dataset_number": 1})
print("Recherche dans Monoprix:")
for item in result1:
    print(item)

result2 = recommend_for_row({"keyword": "eau", "dataset_number": 2})
print("\nRecherche dans Carrefour:")
for item in result2:
    print(item)

result3 = recommend_for_row({"keyword": "eau", "dataset_number": 3})
print("\nRecherche dans Founa:")
for item in result3:
    print(item)