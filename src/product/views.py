from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from src.utils.general_responses import GeneralApiResponse
from .models import Product
from .serializers import ProductSerializer


class Products(APIView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        """
        Caso tenha query params, busca em todos os produtos de acordo com os params válidos
        Caso esteja na rota "product/<:id>" retorna os dados do produto caso a pk exista
        Ex. GET http://localhost:8000/product/?title=a
        Ex. GET http://localhost:8000/product/1
        """
        if self.kwargs.get('product_pk'):
            try:
                product = Product.objects.get(pk=self.kwargs.get('product_pk'))
                serializer = ProductSerializer(product, many=False)
                return JsonResponse(serializer.data, safe=False)
            # o 'objects.get' vai falhar caso o kwarg seja preenchido incorretamente, ou não existir
            except:
                return GeneralApiResponse.bad_request()
        else:
            # TODO refatorar os métodos GET para receberem os query params e model a ser consultado (evitar código duplicado)
            query_params = ['title', 'price', 'brand', 'page']
            request_get_keys = list(request.GET.keys())
            if any(query_param in request_get_keys for query_param in query_params):
                paginator = PageNumberPagination()
                paginator.page_size = 10
                if 'page' not in request_get_keys:
                    paginator.page = 1
                filter_kwargs = dict()
                for query_param in request_get_keys:
                    if query_param != 'page':
                        filter_kwargs[query_param + '__icontains'] = request.GET[query_param]
                products = Product.objects.filter(**filter_kwargs)
                result_page = paginator.paginate_queryset(products, request)
                serializer = ProductSerializer(result_page, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return GeneralApiResponse.bad_request('favor inserir algum parâmetro de busca válido')

    def post(self, request, *args, **kwargs):
        return GeneralApiResponse.bad_request()
