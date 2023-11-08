from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import MyAcccountInfoSerializer
from ..models import UserModel
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from ..permissions import OnlyOwnerAccessIt


class MyAccountInfoView(APIView):
    # IsAithenicated bắt phải đăng nhập mới truy cập vào được

    def get(self, request):
        user = request.user
        serializer = MyAcccountInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = MyAcccountInfoSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})
