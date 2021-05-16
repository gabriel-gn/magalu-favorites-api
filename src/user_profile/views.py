from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.contrib.auth.models import User

from src.user_profile.serializers import UserSerializer
from src.user_profile.tasks import get_user_from_request
from src.utils.general_responses import GeneralApiResponse
from src.utils.permissions import SuperuserPermission


class AuthToken(APIView):
    permission_classes = []
    authentication_classes = []
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Retorna um token de autenticação necessário para fazer chamadas autenticadas
        Incluir "Authotization: Token <valor do token>" no header para fazer chamadas autenticadas
        Ex: POST http://localhost:8000/user/auth
        {
            "email": "gabrielgomesnogueira@gmail.com",
            "password": "gabrielgn"
        }
        """
        required_keys = ['email', 'password']
        request_data_keys = list(request.data.keys())
        if all([key in request_data_keys for key in required_keys]):
            email = request.data['email']
            password = request.data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    pass
                else:
                    return GeneralApiResponse.unauthorized()
            except User.DoesNotExist:
                return GeneralApiResponse.unauthorized()
        else:
            return GeneralApiResponse.bad_request()

        if user is None:
            return GeneralApiResponse.unauthorized()

        # Recria o token toda vez que fizer um login
        try:
            Token.objects.filter(user_id=user.id).delete()
            token, created = Token.objects.get_or_create(user=user)
        except Exception as e:
            return GeneralApiResponse.server_error()
        return JsonResponse({'token': token.key})


class RegisterUser(APIView):
    # Apenas usuários autenticados podem cadastrar novos usuários.
    # Estes devem ser superusuarios
    permission_classes = [SuperuserPermission]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Cria um novo usuário na base.
        Caso o email ja esteja registrado, não completa o registro
        Ex: POST http://localhost:8000/user/register
            {
                "name": "Roberto Almeida do Amaral",
                "email": "robertinho@gmail.com",
                "password": "hello_world*"
            }
        """
        required_keys = ['name', 'email']
        request_data_keys = list(request.data.keys())
        if all([key in request_data_keys for key in required_keys]):
            name = request.data['name']
            email = request.data['email']
            if User.objects.filter(username=email).exists():
                return GeneralApiResponse.conflict()
            # caso não forneça password, é gerado um aleatório, apenas para criar o usuário
            if 'password' in request_data_keys:
                password = request.data['password']
            else:
                password = User.objects.make_random_password()
            splitted_name = name.split(' ')
            first_name = splitted_name[0]
            last_name = ' '.join(splitted_name[1:])
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return JsonResponse({
                'message': 'usuário criado com sucesso',
                'user': user.username
            }, safe=False, status=200)
        else:
            return GeneralApiResponse.bad_request()


class UserActions(APIView):
    # Apenas usuários autenticados podem ver e mexer em dados dos usuários.
    http_method_names = ['get', 'post', 'delete']

    def get(self, request, *args, **kwargs):
        """
        Retorna os dados do usuário autenticado caso não tenha query param
        Caso tenha alguma das query params, filtra na lista de usuarios
        Ex. GET http://localhost:8000/user
        Ex. GET http://localhost:8000/user?first_name=roberto
        """
        query_params = ['username', 'email', 'first_name', 'last_name']
        request_get_keys = list(request.GET.keys())
        if any(query_param in request_get_keys for query_param in query_params):
            filter_kwargs = dict()
            for query_param in request_get_keys:
                filter_kwargs[query_param + '__icontains'] = request.GET[query_param]
            users = User.objects.filter(**filter_kwargs)
            serializer = UserSerializer(users, many=True)
        else:
            serializer = UserSerializer(request.user, many=False)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, *args, **kwargs):
        """
        Apaga o user que fez a requisição se não houver query params
        Caso haja query params, o requisitante seja superuser e a query retornar APENAS 1 resultado, apaga o user.
        Para apagar usuários em massa deve ser usado o django admin ou refinar um pouco mais a api
        Ex. DELETE http://localhost:8000/user/
        """
        query_params = ['username', 'email', 'first_name', 'last_name']
        user, response = get_user_from_request(request, query_params)
        if response:
            return response
        username = user.username
        user.delete()
        return GeneralApiResponse.ok(f'{username} apagado com sucesso!')

    def post(self, request, *args, **kwargs):
        """
        Um usuário pode alterar os próprios dados através da autenticação.
        Um superusuario pode alterar dados de outros usuários caso a query retorne apenas um user
        Se não houver parâmetros de query, tentará alterar o usuário que fez a requisição
        No caso, como o email é único, é a melhor forma de buscar (Essa query é case sensitive)

        Ex. POST http://localhost:8000/user/
        {
            "first_name": "Gabriel",
            "last_name": "Nogueira"
        }

        Ex. POST http://localhost:8000/user/?email=robertinho@gmail.com
        {
            "first_name": "Alberto",
            "last_name": "Santana"
        }
        """
        body = request.data
        body_keys = body.keys()
        updatable_fields = ['username', 'email', 'first_name', 'last_name']
        query_params = ['username', 'email', 'first_name', 'last_name']
        user, response = get_user_from_request(request, query_params)
        if response:
            return response
        # ignora qualquer campo na requisição que não seja os de update do usuário
        for key in body_keys:
            if key in updatable_fields:
                setattr(user, key, body[key])
        user.save()
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)

