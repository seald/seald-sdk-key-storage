from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from views import search, push
import os

app = Starlette(
    debug=os.environ.get("SSKS_DEBUG", "FALSE") == "TRUE",
    routes=[
        Route("/search/", search, methods=["POST"]),
        Route("/push/", push, methods=["POST"]),
    ],
)


@app.exception_handler(404)
@app.exception_handler(400)
async def exception_handler(request, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
