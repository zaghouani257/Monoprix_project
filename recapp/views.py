from django.http import JsonResponse
from django.shortcuts import render
from .models import Monoprix, Carrefour, Founa, Produit
from .RECOMNDATION import recommend_for_row
import json

def search(request):
    return render(request, 'search.html')


def founa(request):
    return render(request, 'founa.html')

def carrefour(request):
    return render(request, 'carrefour.html')  

def recommend(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        dataset_number = int(request.GET.get('dataset_number', '1'))
        page = int(request.GET.get('page', '1'))

        if dataset_number == 1:
            dataset = Monoprix
        elif dataset_number == 2:
            dataset = Carrefour
        elif dataset_number == 3:
            dataset = Founa
        else:
            return JsonResponse({'error': 'Invalid dataset_number.'})

        results, total_pages = recommend_for_row({"keyword": keyword, "dataset_number": dataset_number, "page": page})
        
        if dataset_number == 1:
            response_data = {
                'results': [
                    {
                        'id': int(id),
                        'name': name,
                        'price': price if price is not None else 0,
                        'description': description if description is not None else ''
                    }
                    for id, name, price, description in results
                ],
                'total_pages': total_pages
            }
        elif dataset_number == 2:
            response_data = {
                'results': [
                    {
                        'id': int(id),
                        'name': name,
                        'description': description if description is not None else '',
                        'price': price if price is not None else 0,
                        'brand': brand if brand is not None else ''
                    }
                    for id, name, description, price, brand in results
                ],
                'total_pages': total_pages
            }
        elif dataset_number == 3:
            response_data = {
                'results': [
                    {
                        'id': int(id),
                        'name': name,
                        'description': description if description is not None else '',
                        'price': price if price is not None else 0,
                        'price_before_promos': price_before_promos if price_before_promos is not None else 0
                    }
                    for id, name, description, price, price_before_promos in results
                ],
                'total_pages': total_pages
            }
        else:
            response_data = {'error': 'Invalid dataset_number.'}

        return JsonResponse(response_data)

    elif request.method == 'POST':
        data = json.loads(request.body)
        dataset1_id = data.get('dataset1_id')
        dataset2_info = data.get('dataset2_info')
        dataset3_info = data.get('dataset3_info')

        if dataset1_id is not None:
            try:
                dataset1_item = Monoprix.objects.get(id=dataset1_id)
                if dataset2_info:
                    dataset1_item.similar_product_in_carrefour = dataset2_info['name']
                    dataset1_item.prix_produit_carrefour = dataset2_info['price']
                    dataset1_item.description_produit_carrefour = dataset2_info['description']
                if dataset3_info:
                    dataset1_item.similar_product_in_founa = dataset3_info.get('name')
                    dataset1_item.prix_produit_founa = dataset3_info.get('price')
                    dataset1_item.prix_produit_avant_promos_founa = dataset3_info.get('price_before_promos')
                    dataset1_item.description_produit_founa = dataset3_info.get('description')
                dataset1_item.save()

                # Save the corresponding data to the Produits table
                produits_item = Produit()
                produits_item.code_article = dataset1_item.code_article
                produits_item.similar_product_in_carrefour = dataset2_info.get('name') if dataset2_info else None
                produits_item.prix_produit_carrefour = dataset2_info.get('price') if dataset2_info else None
                produits_item.description_produit_carrefour = dataset2_info.get('description') if dataset2_info else None
                produits_item.similar_product_in_founa = dataset3_info.get('name') if dataset3_info else None
                produits_item.prix_produit_founa = dataset3_info.get('price') if dataset3_info else None
                produits_item.prix_produit_avant_promos_founa = dataset3_info.get('price_before_promos') if dataset3_info else None
                produits_item.description_produit_founa = dataset3_info.get('description') if dataset3_info else None
                produits_item.save()

                return JsonResponse({'success': True})
            except Monoprix.DoesNotExist:
                return JsonResponse({'error': 'Monoprix item not found.'})
        else:
            return JsonResponse({'error': 'Invalid request data.'})

    return JsonResponse({'error': 'Invalid request method.'})

def get_dataset1_data(request):
    dataset1_items = Monoprix.objects.all()
    response_data = {
        'results': [
            {
                'libelle_article': item.libelle_article,
                'similar_product_in_carrefour': item.similar_product_in_carrefour,
                'prix_produit_carrefour': item.prix_produit_carrefour,
                'description_produit_carrefour': item.description_produit_carrefour,
                'similar_product_in_founa': item.similar_product_in_founa,
                'prix_produit_founa': item.prix_produit_founa,
                'description_produit_founa': item.description_produit_founa,
            }
            for item in dataset1_items
        ]
    }
    return JsonResponse(response_data)

