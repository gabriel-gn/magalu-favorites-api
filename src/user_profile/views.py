from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.contrib.auth.models import User

from src.user_profile.serializers import UserSerializer
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
        Ex: POST http://localhost:8000/u/auth
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
        Ex: POST http://localhost:8000/u/register
            {
                "name": "Roberto Almeida do Amaral",
                "email": "robertinho@gmail.com",
                "password": "hello_world*"
            }
        """
        required_keys = ['name', 'email', 'password']
        request_data_keys = list(request.data.keys())
        if all([key in request_data_keys for key in required_keys]):
            name = request.data['name']
            email = request.data['email']
            if User.objects.filter(username=email).exists():
                return GeneralApiResponse.conflict()
            password = request.data['password']
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
    # Apenas usuários autenticados podem ver dados dos usuários.
    http_method_names = ['get', 'post', 'delete']

    def get(self, request, *args, **kwargs):
        """
        Retorna os dados do usuário autenticado caso não tenha query param
        Caso tenha alguma das query params, filtra na lista de usuarios
        Ex. GET http://localhost:8000/u
        Ex. GET http://localhost:8000/u?first_name=roberto
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

