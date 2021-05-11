from rest_framework import status
from rest_framework.response import Response


class GeneralApiResponse:

    @staticmethod
    def ok():
        return Response({'message': 'solicitação concluída'}, status=status.HTTP_200_OK)

    @staticmethod
    def bad_request():
        return Response({'message': 'requisição inválida'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def unauthorized():
        return Response({'message': 'você não está autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden():
        return Response({'message': 'você não tem permissão para acessar'}, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def conflict():
        return Response({'message': 'já existente'}, status=status.HTTP_409_CONFLICT)

    @staticmethod
    def server_error():
        return Response({'message': 'ocorreu um erro ao processar sua requisição'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)