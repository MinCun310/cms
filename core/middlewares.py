from account.models.model_blacklist_token import BlacklistedTokenModel
from rest_framework.exceptions import APIException
from django.http import HttpResponse, JsonResponse


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # nếu có gửi lên token thì bắt đầu kiểm tra
        if "Authorization" in request.headers:
            # xác thực token, xem thử token có nằm trong blacklisted không ?
            # Nếu có thì response 403, message : Token is blacklisted
            access_token = request.headers["Authorization"].split()[1]

            if BlacklistedTokenModel.is_token_blacklisted(access_token):
                return JsonResponse(
                    {"message": "Access token is blacklisted"}, status=403
                )
        response = self.get_response(request)
        return response
