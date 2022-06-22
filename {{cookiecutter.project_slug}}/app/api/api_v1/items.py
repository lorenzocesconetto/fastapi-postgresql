from app import crud, models, schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items", tags=["items"])


def get_item(*, db: Session = Depends(deps.get_db), id: int) -> models.Item:
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item


@router.get("/", response_model=list)
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    user: models.User = Depends(deps.get_current_active_user),
):
    """Retrieve items."""
    if crud.user.is_superuser(user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(db, owner_id=user.id, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    user: models.User = Depends(deps.get_current_active_user),
):
    """Create new item."""
    return crud.item.create_with_owner(db, obj_in=item_in, owner_id=user.id)


@router.patch("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item: models.Item = Depends(get_item),
    item_in: schemas.ItemUpdate,
    user: models.User = Depends(deps.get_current_active_user),
):
    """Update an item."""
    if not crud.user.is_superuser(user) and (item.owner_id != user.id):
        raise HTTPException(status_code=400, detail="This item belongs to another user")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    item: models.Item = Depends(get_item),
    user: models.User = Depends(deps.get_current_active_user),
):
    """Get item by id."""
    if not crud.user.is_superuser(user) and (item.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions.")
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item: models.Item = Depends(get_item),
    user: models.User = Depends(deps.get_current_active_user),
):
    """Delete an item."""
    if not crud.user.is_superuser(user) and (item.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.remove(db=db, id=item.id)
    return item
