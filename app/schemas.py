from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AdvertisementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    author: str = Field(..., min_length=1, max_length=100)


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, ge=0)
    author: Optional[str] = Field(None, min_length=1, max_length=100)


class AdvertisementOut(AdvertisementBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)