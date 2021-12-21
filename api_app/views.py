from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TestApiView(APIView):
    def post(self, request):
        return Response({"status": "success", "data": "test"}, status=status.HTTP_200_OK)
