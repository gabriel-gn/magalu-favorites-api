from django.urls import path

from src.product.views import *

app_name = 'product'
urlpatterns = [
    # API REST
    path('', Products.as_view(), name='products_index'),
]