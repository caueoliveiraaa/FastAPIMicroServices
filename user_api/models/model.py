from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserRequest(BaseModel):
    full_name: str
    cpf: str
    email: str
    phone_number: Optional[str]

    class Config:
        from_attributes = True
