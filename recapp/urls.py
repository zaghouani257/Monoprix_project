from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
    path('', views.search, name='search'), 
    path('founa/', views.founa, name='founa'),
    path('carrefour/', views.carrefour, name='carrefour'),
    path('get_dataset1_data/', views.get_dataset1_data, name='get_dataset1_data'),
   
]
