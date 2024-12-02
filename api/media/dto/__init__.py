from pydantic import BaseModel


class UrlResponseDTO(BaseModel):
    url: str


class FilenameResponseDTO(BaseModel):
    filename: str
