from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    error = "%s %s %s" % (context['view'], context['request'].method, exc)
    if response is None:
        return Response(
            {"error": "刷新一下马上就好了！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
    return response
