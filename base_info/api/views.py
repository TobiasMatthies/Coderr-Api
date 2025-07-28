from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from . serializers import BaseInfoSerializer


class BaseInfoAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        """
        Returns the base info of the API.

        :param request: The request object
        :return: A Response object with the base info
        """
        serializer = BaseInfoSerializer(instance={})
        return Response(serializer.data, status=status.HTTP_200_OK)
