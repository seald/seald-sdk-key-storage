from starlette.applications import Starlette
from starlette.routing import Route

from views import search, push

app = Starlette(debug=True, routes=[
    Route('/search/', search, methods=["POST"]),
    Route('/push/', push, methods=["POST"]),
])
