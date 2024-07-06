from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    serial_number: str
    product_name: str
    input_image_urls: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    request_id: int
    output_image_urls: Optional[str] = None

    class Config:
        orm_mode = True

class RequestBase(BaseModel):
    request_id: str
    status: str

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    created_at: str
    updated_at: str
    products: List[Product] = []

    class Config:
        orm_mode = True

class ProcessedImageResponse(BaseModel):
    request_id: str

class StatusResponse(BaseModel):
    status: str
