from django.urls import path

from src.products.views import *

app_name = 'products'
urlpatterns = [
    # API REST
    path('', Products.as_view(), name='products_index'),
]