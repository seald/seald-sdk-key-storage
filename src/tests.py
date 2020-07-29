import os
import shutil
import unittest
from unittest import mock

from starlette.testclient import TestClient
from sealdsdkstorage import app

client = TestClient(app)


@mock.patch.dict(os.environ, {"SSKS_BASE_DIR": "../data-tests"})
class SealdSdkStorageTestCase(unittest.TestCase):
    def setUp(self):
        os.mkdir("../data-tests")

    def tearDown(self):
        shutil.rmtree("../data-tests")

    def test01_endpoints(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 404)
        response = client.get("/search/")
        self.assertNotEqual(response.status_code, 404)
        response = client.get("/push/")
        self.assertNotEqual(response.status_code, 404)

    def test02_json(self):
        response = client.post("/search/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Body is not JSON")
        response = client.post("/search/", json={})
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.json()["detail"], "Body is not JSON")
        response = client.post("/push/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Body is not JSON")
        response = client.post("/push/", json={})
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.json()["detail"], "Body is not JSON")

    def test02_push_retrieve(self):
        response = client.post(
            "/push/",
            json={
                "app_id": "app_id",
                "username": "username",
                "secret": "secret",
                "data_b64": "random/data",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        response = client.post(
            "/search/",
            json={"app_id": "app_id", "username": "username", "secret": "secret",},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data_b64"], "random/data")

    def test03_multi_user_update(self):
        response = client.post(
            "/push/",
            json={
                "app_id": "app_id",
                "username": "username1",
                "secret": "secret1",
                "data_b64": "random/data1",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        response = client.post(
            "/push/",
            json={
                "app_id": "app_id",
                "username": "username2",
                "secret": "secret2",
                "data_b64": "random/data2",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        response = client.post(
            "/push/",
            json={
                "app_id": "app_id",
                "username": "username1",
                "secret": "secret1",
                "data_b64": "random/data3",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        response = client.post(
            "/search/",
            json={"app_id": "app_id", "username": "username1", "secret": "secret1",},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data_b64"], "random/data3")
        response = client.post(
            "/search/",
            json={"app_id": "app_id", "username": "username2", "secret": "secret2",},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data_b64"], "random/data2")

    def test04_does_not_exists(self):
        response = client.post(
            "/search/",
            json={"app_id": "no_app", "username": "username1", "secret": "secret1",},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not found")
