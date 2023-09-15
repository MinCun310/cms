from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import MyAcccountInfoSerializer
from ..models import UserModel
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class MyAccountInfoView(APIView):
    # IsAithenicated bắt phải đăng nhập mới truy cập vào được
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user
        profile = UserModel.objects.get(id=user.id)
        serializer = MyAcccountInfoSerializer(profile)
        return Response(serializer.data)
        