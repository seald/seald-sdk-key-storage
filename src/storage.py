import os

from starlette.exceptions import HTTPException


async def store(app_id, username, secret, data_b64):
    path = os.environ.get("SSKS_BASE_DIR", "/ssks-data")
    for sub_dir in [app_id, username]:
        path = os.path.join(path, sub_dir)
        if not os.path.exists(path):
            os.makedirs(path)
    path = os.path.join(path, secret)
    with open(path, "w") as file:
        file.write(data_b64)


async def retrieve(app_id, username, secret):
    path = os.path.join(
        os.environ.get("SSKS_BASE_DIR", "data"), app_id, username, secret
    )
    try:
        with open(path, "r") as file:
            data_b64 = file.read()
    except FileNotFoundError:
        raise HTTPException(404, "Not found")
    return data_b64
