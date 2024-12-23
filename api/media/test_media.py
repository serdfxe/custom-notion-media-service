import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi import FastAPI
from api.media import media_router, s3_manager
from tempfile import NamedTemporaryFile

app = FastAPI()
app.include_router(media_router)

s3_manager.generate_presigned_url = MagicMock()
s3_manager.upload_file = MagicMock()
s3_manager.delete_file = MagicMock()

client = TestClient(app)


@pytest.fixture
def user_id():
    return str(uuid4())

@pytest.fixture
def file_id():
    return str(uuid4())

@pytest.fixture
def headers(user_id):
    return {"X-User-Id": user_id}


def test_get_media_url_success(user_id, headers, file_id):
    s3_manager.generate_presigned_url.return_value = "https://example.com/media"

    response = client.get(f"/media/{user_id}/{file_id}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"url": "https://example.com/media"}
    s3_manager.generate_presigned_url.assert_called_once_with(key=f"{user_id}/{file_id}")


def test_get_media_url_unauthorized(file_id, user_id):
    response = client.get(f"/media/{user_id}/{file_id}", headers={})

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_get_media_url_not_found(user_id, headers, file_id):
    s3_manager.generate_presigned_url.side_effect = Exception()

    response = client.get(f"/media/{user_id}/{file_id}", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_upload_media_success(user_id, headers):
    s3_manager.upload_file.return_value = "https://example.com/media"

    with NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(b"test content")
        temp_file.seek(0)
        response = client.post("/media", files={"file": temp_file}, headers=headers)

    assert response.status_code == 201
    assert response.json() == {"url": "https://example.com/media"}
    s3_manager.upload_file.assert_called_once()


def test_upload_media_unauthorized():
    with NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(b"test content")
        temp_file.seek(0)
        response = client.post("/media", files={"file": temp_file}, headers={})

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_delete_media_success(user_id, headers, file_id):
    response = client.delete(f"/media/{user_id}/{file_id}", headers=headers)

    assert response.status_code == 200
    s3_manager.delete_file.assert_called_once_with(f"{user_id}/{file_id}")


def test_delete_media_unauthorized(file_id, user_id):
    response = client.delete(f"/media/{user_id}/{file_id}", headers={})

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized."


def test_delete_media_not_found(user_id, headers):
    s3_manager.delete_file.side_effect = Exception()

    response = client.delete(f"/media/{user_id}/{user_id}", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"