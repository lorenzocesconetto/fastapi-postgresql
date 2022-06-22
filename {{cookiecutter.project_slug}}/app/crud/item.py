from app.crud.base import CRUDBaseWithOwner
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

item = CRUDBaseWithOwner[Item, ItemCreate, ItemUpdate](Item)
