import boto3
import os

from tempfile import NamedTemporaryFile

from core.config import S3_HOST


class S3Manager:
    def __init__(
        self,
        bucket_name: str,
        access_key_id: str,
        secret_access_key: str,
        endpoint_url: str,
    ):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )

    def upload_file(self, file, key: str) -> str:
        """
        Upload file.
        """
        temp = NamedTemporaryFile(delete=False)

        contents = file.file.read()
        with temp as f:
            f.write(contents)
        file.file.close()

        self.s3_client.upload_file(temp.name, Bucket=self.bucket_name, Key=key)

        os.remove(temp.name)

        return f"{S3_HOST}/{self.bucket_name}/{key}"

    def delete_file(self, key: str) -> None:
        """
        Delete file.
        """
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)

    def generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """
        Generate presigned url with expiration time.
        """
        self.s3_client.head_object(Bucket=self.bucket_name, Key=key)

        response = self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expiration,
        )

        return response
