import logging
from uuid import UUID
from fastapi import APIRouter, File, Request, UploadFile, HTTPException

from .dto import MediaResponseDTO

from core.s3 import S3Manager
from core.config import BUCKET_NAME, ACCESS_KEY_ID, SECRET_ACCESS_KEY, S3_HOST

s3_manager = S3Manager(
    bucket_name=BUCKET_NAME,
    access_key_id=ACCESS_KEY_ID,
    secret_access_key=SECRET_ACCESS_KEY,
    endpoint_url=S3_HOST,
)

media_router = APIRouter(prefix="/media", tags=["media"])


@media_router.get("/{user_id}/{file_id}", response_model=MediaResponseDTO, responses={
    200: {"description": "Success."},
    401: {"description": "Unauthorized."},
    404: {"description": "Not Found."},
})
async def get_media_url_route(user_id: UUID, file_id: UUID, request: Request):
    """
    Get media URL. The operation returns the media URL which is associated with user_id (is equal to X-User-Id in header) and file_id.
    """
    if request.headers.get("X-User-Id") != str(user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")

    media_url = s3_manager.generate_presigned_url(key=f"{user_id}/{file_id}")

    if media_url is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"url": media_url}


@media_router.post("", response_model=MediaResponseDTO, responses={
    201: {"description": "Successfully uploaded."},
    401: {"description": "Unauthorized."},
})
async def upload_media_route(request: Request, file: UploadFile = File(...)):
    """
    Upload media.
    """
    if request.headers.get("X-User-Id") is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        media_url = s3_manager.upload_file(file=file, key=f"{request.headers.get('X-User-Id')}/{file.filename}")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Error on uploading the file")


    return {"url": media_url}


@media_router.delete("", responses={
    200: {"description": "Successfully deleted."},
    401: {"description": "Unauthorized."},
    404: {"description": "Not Found."},
})
async def delete_media_route(request: Request, file: UploadFile = File(...)):
    """
    Delete media.
    """
    if request.headers.get("X-User-Id") is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        s3_manager.delete_file(key=f"{request.headers.get('X-User-Id')}/{file.filename}")
    except Exception:
        raise HTTPException(status_code=404, detail="Not found")
