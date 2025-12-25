from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    PDF = "pdf"
    GIF = "gif"

class MediaItem(BaseModel):
    url: str
    type: MediaType



class PostCreate(BaseModel):
    caption: Optional[str] = Field(None, max_length=300)
    media: List[MediaItem] = Field(..., min_items =1)

