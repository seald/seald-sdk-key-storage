import os

BASE_DIR = os.environ.get("SSKS_BASE_DIR", "data")


async def store(app_id, username, secret, data_b64):
    path = BASE_DIR
    if not os.path.exists(path):
        os.makedirs(path)
    for sub_dir in [app_id, username]:
        path = os.path.join(path, sub_dir)
        if not os.path.exists(path):
            os.makedirs(path)
    path = os.path.join(path, secret)
    with open(path, "w") as file:
        file.write(data_b64)


async def retrieve(app_id, username, secret):
    path = os.path.join(BASE_DIR, app_id, username, secret)
    with open(path, "r") as file:
        data_b64 = file.read()
    return data_b64
