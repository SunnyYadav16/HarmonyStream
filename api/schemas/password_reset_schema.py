
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class PasswordRequestResetSchema(BaseModel):
    email: EmailStr


class PasswordResetSchema(PasswordRequestResetSchema):
    otp: str
    new_password: str
    confirm_password: str
