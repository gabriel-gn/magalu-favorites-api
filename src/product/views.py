from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from src.utils.general_responses import GeneralApiResponse
from .models import Product, UserFavorites
from .serializers import ProductSerializer
from ..user_profile.tasks import get_user_from_request


class Products(APIView):
    permission_classes = []
    authentication_classes = []
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
            # assim como no "get_user_from_request()"
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
                products = Product.objects.filter(**filter_kwargs).order_by('pk')
                result_page = paginator.paginate_queryset(products, request)
                serializer = ProductSerializer(result_page, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return GeneralApiResponse.bad_request('favor inserir algum parâmetro de busca válido')

    def post(self, request, *args, **kwargs):
        # não será implementado adição de produtos pela API por enquanto
        # Para adicionar novos produtos, utilizar o django seed, ou criar script para adicionar chamando o django,
        # ou utilizar o django admin para isso manualmente!!
        return GeneralApiResponse.bad_request()


class UserFavoritesView(APIView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        """
        Retorna a lista de desejos do usuário que fez a requisição
        Caso tenha alguma das query params, filtra na lista de usuarios CASO o requisitante seja superuser
        Ex. GET http://localhost:8000/product/favorites
        Ex. GET http://localhost:8000/product/favorites?email=gabrielgomesnogueira@gmail.com
        """
        query_params = ['username', 'email', 'first_name', 'last_name', 'page']
        user, response = get_user_from_request(request, query_params)
        if response:
            return response
        user_favorites_products = UserFavorites.objects.get(user=user).products.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(user_favorites_products, request)
        serializer = ProductSerializer(result_page, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        """
        Ex. POST http://localhost:8000/product/favorites?email=gabrielgomesnogueira@gmail.com
        Ex. POST http://localhost:8000/product/favorites
        {
            "action": "add",
            "products": [
                1,
                2,
                3
            ]
        }
        """
        if all([key in request.data.keys() for key in ['action', 'products']]):
            query_params = ['username', 'email', 'first_name', 'last_name']
            user, response = get_user_from_request(request, query_params)
            if response:
                return response
            try:
                if request.data['action'] == 'add':
                    products = Product.objects.filter(pk__in=request.data['products'])
                    user.userfavorites.products.add(*list(products))
                    return GeneralApiResponse.ok('produtos incluídos com sucesso')
                elif request.data['action'] == 'remove':
                    products = Product.objects.filter(pk__in=request.data['products'])
                    user.userfavorites.products.remove(*list(products))
                    return GeneralApiResponse.ok('produtos removidos com sucesso')
                else:
                    return GeneralApiResponse.bad_request("o valor do parâmetro 'action' deve ser 'add' ou 'remove'")
            except:
                return GeneralApiResponse.server_error()
        else:
            return GeneralApiResponse.bad_request("necessário incluir 'action' e 'products' no payload")