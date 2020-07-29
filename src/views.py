from starlette.responses import JSONResponse

from serializers import validate, PushSerializer, SearchSerializer
from storage import retrieve, store


async def push(request):
    data = await validate(PushSerializer, request)
    await store(
        app_id=data["app_id"],
        username=data["username"],
        secret=data["secret"],
        data_b64=data["data_b64"],
    )
    return JSONResponse({"status": "ok"})


async def search(request):
    data = await validate(SearchSerializer, request)
    data_b64 = await retrieve(
        app_id=data["app_id"],
        username=data["username"],
        secret=data["secret"],
    )
    return JSONResponse({"data_b64": data_b64})
