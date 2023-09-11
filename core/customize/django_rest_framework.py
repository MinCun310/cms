from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    # if isinstance(exc, Ratelimited):
    #     print(exc)
    #     return Response({"message": "Blocked"}, status=429)

    if isinstance(exc, exceptions.APIException) and isinstance(exc.detail, (list, dict)):
        response.data = {
            "error_fields": response.data
        }

    return response