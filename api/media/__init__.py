from typing import Annotated
from uuid import UUID, uuid4
from fastapi import APIRouter, File, Header, Request, UploadFile, HTTPException
from fastapi.responses import StreamingResponse 

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
    responses={
        200: {
            "description": "Success.",
            "content": {"*/*": {}}
        },
        401: {"description": "Unauthorized."},
        404: {"description": "Not Found."},
    },
)
async def get_media_file(
    filename: str,
    x_user_id: Annotated[str, Header()]
):
    """
    Get media file. Can be used as src in HTML tags like <img>, <video>, etc.
    """
    try:
        file_obj = s3_manager.s3_client.get_object(
            Bucket=s3_manager.bucket_name,
            Key=f"{x_user_id}/{filename}",
        )
        
        content_type = "application/octet-stream"
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            content_type = f"image/{filename.split('.')[-1].lower()}"
        elif filename.lower().endswith('.mp4'):
            content_type = "video/mp4"
        elif filename.lower().endswith('.pdf'):
            content_type = "application/pdf"
        
        return StreamingResponse(
            file_obj['Body'].iter_chunks(),
            media_type=content_type,
            headers={
                "Content-Disposition": f"inline; filename={filename}"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")


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

    content_type = file.content_type or "application/octet-stream"

    await s3_manager.upload_file(file=file, key=f"{x_user_id}/{filename}", ContentType=content_type)
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
