from urllib.request import Request

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def get_routes(request: Request) -> Response:
    routes = ["abc"]

    return Response(routes)
