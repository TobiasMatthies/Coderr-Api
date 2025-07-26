from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from . serializers import BaseInfoSerializer


class BaseInfoAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        serializer = BaseInfoSerializer(instance={})
        return Response(serializer.data, status=status.HTTP_200_OK)
