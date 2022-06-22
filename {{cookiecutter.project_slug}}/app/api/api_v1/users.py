from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.mail import send_new_account_email

router = APIRouter(prefix="/users", tags=["users"])


def get_user(*, db: Session = Depends(deps.get_db), user_id: int):
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.get(
    "",
    response_model=list[schemas.User],
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """Retrieve users."""
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    """Create new user without the need to be logged in."""
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server.",
        )
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    return crud.user.create(db, obj_in=user_in)


@router.post(
    "", response_model=schemas.User, dependencies=[Depends(deps.get_current_active_superuser)]
)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserAdminCreate,
):
    """Create new user."""
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(email_to=user_in.email, username=user_in.email)
    return user


@router.patch("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    user: models.User = Depends(deps.get_current_active_user),
):
    """Update own user."""
    return crud.user.update(db, db_obj=user, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
def read_user_me(user: models.User = Depends(deps.get_current_active_user)):
    """Get current user."""
    return user


@router.get(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def read_user_by_id(user: models.User = Depends(get_user)):
    """Get a specific user by id."""
    return user


@router.put(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(get_user),
    user_in: schemas.UserUpdate,
):
    """Update a user."""
    return crud.user.update(db, db_obj=user, obj_in=user_in)
