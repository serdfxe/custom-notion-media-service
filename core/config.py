import os
from dotenv import load_dotenv


load_dotenv(override=True)


DEBUG: bool = os.environ.get("DEBUG", "False") == "True"
API_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")
API_PORT: int = int(os.environ.get("APP_PORT", "8000"))

S3_HOST: str = os.environ.get("S3_HOST")
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
