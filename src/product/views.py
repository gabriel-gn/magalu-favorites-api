from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView

from src.utils.general_responses import GeneralApiResponse
from .models import Product
from .serializers import ProductSerializer


class Products(APIView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        """
        Ex. GET http://localhost:8000/product/?title=a
        """
        # TODO refatorar os métodos GET para receberem os query params e model a ser consultado (evitar código duplicado)
        query_params = ['title', 'price', 'brand']
        request_get_keys = list(request.GET.keys())
        if any(query_param in request_get_keys for query_param in query_params):
            filter_kwargs = dict()
            for query_param in request_get_keys:
                filter_kwargs[query_param + '__icontains'] = request.GET[query_param]
            products = Product.objects.filter(**filter_kwargs)
            serializer = ProductSerializer(products, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return GeneralApiResponse.bad_request('favor inserir algum parâmetro de busca válido')

    def post(self, request, *args, **kwargs):
        return GeneralApiResponse.bad_request()
