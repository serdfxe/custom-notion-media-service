from typing import Annotated
from uuid import UUID, uuid4
from fastapi import APIRouter, File, Header, Request, UploadFile, HTTPException

from .dto import FilenameResponseDTO, UrlResponseDTO

from core.s3 import S3Manager
from core.config import BUCKET_NAME, ACCESS_KEY_ID, SECRET_ACCESS_KEY, S3_HOST

s3_manager = S3Manager(
    bucket_name=BUCKET_NAME,
    access_key_id=ACCESS_KEY_ID,
    secret_access_key=SECRET_ACCESS_KEY,
    endpoint_url=S3_HOST,
)

media_router = APIRouter(prefix="/media", tags=["media"])


@media_router.get(
    "/{filename}",
    response_model=UrlResponseDTO,
    responses={
        200: {"description": "Success."},
        401: {"description": "Unauthorized."},
        404: {"description": "Not Found."},
    },
)
async def get_media_url_route(
    filename: str, x_user_id: Annotated[str, Header()], request: Request
):
    """
    Get media URL. The operation returns the media URL which is associated with
    user_id (is equal to X-User-Id in header) and file_id.
    """
    # try:
    media_url = s3_manager.generate_presigned_url(key=f"{x_user_id}/{filename}")
    # except Exception:
    #    raise HTTPException(status_code=404, detail="Not found")

    return {"url": media_url}


@media_router.post(
    "",
    status_code=201,
    response_model=FilenameResponseDTO,
    responses={
        201: {"description": "Successfully uploaded."},
        401: {"description": "Unauthorized."},
    },
)
async def upload_media_route(
    request: Request, x_user_id: Annotated[str, Header()], file: UploadFile = File(...)
):
    """
    Upload media.
    """
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # try:

    filename = f"{str(uuid4())}-{file.filename}"

    await s3_manager.upload_file(file=file, key=f"{x_user_id}/{filename}")
    # except Exception:
    #    raise HTTPException(status_code=500, detail="Error on uploading the file")

    return {"filename": filename}


@media_router.delete(
    "/{user_id}/{filename}",
    responses={
        200: {"description": "Successfully deleted."},
        401: {"description": "Unauthorized."},
        404: {"description": "Not Found."},
    },
)
async def delete_media_route(
    user_id: UUID, x_user_id: Annotated[str, Header()], filename: str, request: Request
):
    """
    Delete media.
    """
    if x_user_id != str(user_id):
        raise HTTPException(status_code=401, detail="Unauthorized.")

    try:
        s3_manager.delete_file(f"{user_id}/{filename}")
    except Exception:
        raise HTTPException(status_code=404, detail="Not Found")
