from pydantic import BaseModel, EmailStr

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
class UserCreate(BaseModel):
    photo: str

class UserRead(BaseModel):
    id: int
    photo: str  # JSON string containing file_path and face_encoding

    class Config:
        from_attributes = True  # Updated for Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"