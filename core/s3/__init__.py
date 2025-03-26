import boto3
from typing import Optional


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

    async def upload_file(self, file, key: str, **kwargs):
        """
        Upload file.
        """
        self.s3_client.put_object(Body=await file.read(), Bucket=self.bucket_name, Key=key, **kwargs)

    def delete_file(self, key: str):
        """
        Delete file.
        """
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)

    def generate_presigned_url(self, key: str, expiration: int = 3600, **kwargs) -> Optional[str]:
        """
        Generate presigned url with expiration time.
        """
        self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
        
        response = self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key, **kwargs},
            ExpiresIn=expiration,
        )

        return response
