from uuid import UUID
from fastapi import APIRouter, File, Request, UploadFile

from .dto import MediaResponseDTO


media_router = APIRouter(prefix="/media", tags=["media"])

@media_router.get("/{user_id}/{file_id}", response_model=MediaResponseDTO, responses={
    200: {"description": "Sucess."},
    401: {"description": "Unauthorized."},
    404: {"description": "Not Found."},
})
async def get_media_url_route(user_id: UUID, file_id: UUID, request: Request):
    """
    Get media URL. The operation returns the media URL wich is associated with user_id (is equal to X-User-Id in header) and file_id.
    """

@media_router.post("", response_model=MediaResponseDTO, responses={
    201: {"description": "Sucessfully uploaded."},
    401: {"description": "Unauthorized."},
})
async def upload_media_route(request: Request, file: UploadFile = File(...)):
    """
    Upload media.
    """

@media_router.delete("", responses={
    200: {"description": "Sucessfully deleted."},
    401: {"description": "Unauthorized."},
    404: {"description": "Not Found."},
})
async def delete_media_route(request: Request, file: UploadFile = File(...)):
    """
    Upload media.
    """