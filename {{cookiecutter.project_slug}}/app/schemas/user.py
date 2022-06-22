from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    full_name: str | None = None


# Properties to receive via API on creation.
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Only admin should be able to set is_active and is_superuser when creating a user.
class UserAdminCreate(UserCreate):
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserUpdateHashedPassword(UserBase):
    hashed_password: str | None = None


# Only admin should be able to modify is_active and is_superuser
class UserAdminUpdate(UserUpdate):
    is_active: bool = True
    is_superuser: bool = False


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    email: EmailStr
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


# Additional properties to return to client via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(User):
    hashed_password: str
