from pydantic import BaseModel


class MediaResponseDTO(BaseModel):
    url: str