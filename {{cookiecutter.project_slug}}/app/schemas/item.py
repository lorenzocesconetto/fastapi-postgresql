from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: str | None = None
    description: str | None = None


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive via API on update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Additional properties to return to client via API
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
