from typing import Tuple

from django.contrib.auth.models import User

from src.utils.general_responses import GeneralApiResponse


def get_user_from_request(request, available_query_params: list()) -> Tuple[User, GeneralApiResponse]:
    """
    Entra com o request da view e uma lista de query params do user que podem ser consultados
    Retorna um user caso seja si mesmo, ou tenha permissão de acesso a outros usuários
    Retorna uma resposta de erro caso algo não possa ser completado
    """
    get_keys = list(request.GET.keys())
    if len(get_keys) > 0:
        if request.user.is_superuser:
            if any(query_param not in available_query_params for query_param in get_keys):
                return None, GeneralApiResponse.bad_request()  # algum query param na requisição de user ta zoado
            users = User.objects.filter(**request.GET.dict())
            if not users.exists():
                return None, GeneralApiResponse.not_found()  # não achou usuário que atendesse à query
            elif len(users) > 1:
                return None, GeneralApiResponse.bad_request()  # query retornou mais de um usuário para alterar
            else:
                return users[0], None
        else:
            return None, GeneralApiResponse.unauthorized()
    else:
        return request.user, None
