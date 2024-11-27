import os
from dotenv import load_dotenv


load_dotenv(override=True)


DEBUG: bool = os.environ.get("DEBUG", "False") == "True"
API_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")
API_PORT: int = int(os.environ.get("APP_PORT", "8000"))

S3_HOST: str = os.environ.get("S3_HOST", "https://s3.timeweb.cloud")
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID", "C3XGFRE06D0M0PS8SMDX")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY", "SfK3YsoNUNf21vAENk9pddrsG2adId7qqpC0e4pD")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "20ec8cb9-f7c")
