from rest_framework import status
from rest_framework.response import Response


class GeneralApiResponse:

    @staticmethod
    def ok(message='solicitação concluída'):
        return Response({'message': message}, status=status.HTTP_200_OK)

    @staticmethod
    def bad_request(message='requisição inválida'):
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def unauthorized():
        return Response({'message': 'você não está autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden():
        return Response({'message': 'você não tem permissão para acessar'}, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def not_found():
        return Response({'message': 'não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def conflict():
        return Response({'message': 'já existente'}, status=status.HTTP_409_CONFLICT)

    @staticmethod
    def server_error():
        return Response({'message': 'ocorreu um erro ao processar sua requisição'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)