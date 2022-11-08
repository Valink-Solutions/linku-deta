from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from nanoid import generate


class User(BaseModel):
    email: str