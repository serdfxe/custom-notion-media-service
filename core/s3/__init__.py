import boto3


class S3Manager:
    def __init__(self, bucket_name: str, access_key_id: str, secret_access_key: str, endpoint_url: str):
        self.bucket_name = bucket_name
        print(bucket_name, access_key_id, secret_access_key, endpoint_url)
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )

    def upload_file(self, file, key: str) -> str:
        """
        Upload file.
        """

    def delete_file(self, key: str) -> None:
        """
        Delete file.
        """

    def generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """
        Generate presigned url with expiration time.
        """
