from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderRequest(BaseModel):
    user_id: int
    item_description: str
    item_quantity: int
    item_price: float

    class Config:
        from_attributes = True
