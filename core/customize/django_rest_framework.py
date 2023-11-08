from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django_ratelimit.exceptions import Ratelimited
from account.config.constants import ERROR_CODE


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if isinstance(exc, Ratelimited):
        return Response(
            {
                "status": False,
                "message": "Don't access it too much, please try again later",
                "error_code": ERROR_CODE["RATE_LIMIT_CLICK"],
            },
            status=429,
        )
    if isinstance(exc, exceptions.APIException) and isinstance(
        exc.detail, (list, dict)
    ):
        response.data = {"error_fields": response.data}

    return response
