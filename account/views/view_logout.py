from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import BlacklistedTokenModel
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from django.contrib.auth import logout


class LogoutViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_token = request.headers.get("Authorization").split()[1]
        BlacklistedTokenModel.objects.create(token=access_token)
        logout(request)
        return Response({"message": "Logout success!!"})
