import pytest
from unittest.mock import MagicMock, patch, mock_open
from tempfile import TemporaryFile

from moto.efs.urls import response

from core.s3 import S3Manager
from core.config import S3_HOST

@pytest.fixture
def s3_manager():
    bucket_name = "test-bucket"
    access_key_id = "test-access-key"
    secret_access_key = "test-secret-key"
    endpoint_url = "http://test-endpoint-url"
    manager = S3Manager(
        bucket_name=bucket_name,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        endpoint_url=endpoint_url,
    )
    manager.s3_client = MagicMock()
    return manager

@patch("tempfile.NamedTemporaryFile")
def test_upload_file(mock_tempfile, s3_manager):
    temp_file = TemporaryFile()
    mock_tempfile.return_value = temp_file

    mock_file = MagicMock()
    mock_file.file.read.return_value = b"test file content"

    key = "test-key"
    result = s3_manager.upload_file(file=mock_file, key=key)

    mock_file.file.read.assert_called_once()

    assert result == f"{S3_HOST}/{s3_manager.bucket_name}/{key}"

def test_delete_file(s3_manager):
    key = "test-key"

    s3_manager.delete_file(key)

    s3_manager.s3_client.delete_object.assert_called_once_with(
        Bucket=s3_manager.bucket_name, Key=key
    )

def test_generate_presigned_url(s3_manager):
    key = "test-key"
    expiration = 3600

    s3_manager.s3_client.generate_presigned_url.return_value = "http://presigned-url"

    result = s3_manager.generate_presigned_url(key=key, expiration=expiration)

    s3_manager.s3_client.head_object.assert_called_once_with(
        Bucket=s3_manager.bucket_name, Key=key
    )
    s3_manager.s3_client.generate_presigned_url.assert_called_once_with(
        "get_object",
        Params={"Bucket": s3_manager.bucket_name, "Key": key},
        ExpiresIn=expiration,
    )

    assert result == "http://presigned-url"
