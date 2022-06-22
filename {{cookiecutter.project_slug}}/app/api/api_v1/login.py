from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.security import (
    generate_password_reset_token,
    get_password_hash,
    verify_password_reset_token,
)
from app.mail import send_reset_password_email

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """OAuth2 compatible token login, get an access token for future requests."""
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password."
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user.")
    return {"access_token": security.create_access_token(str(user.id)), "token_type": "bearer"}


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_active_user)):
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(*, db: Session = Depends(deps.get_db), email: EmailStr):
    user = crud.user.get_by_email(db, email=email)
    password_reset_token = generate_password_reset_token(email=email)
    if user:
        send_reset_password_email(email_to=user.email, email=email, token=password_reset_token)
    return {"msg": "If this email is registered within our system, you'll get an recovery email."}


@router.post("/reset-password", response_model=schemas.Msg)
def reset_password(
    *, db: Session = Depends(deps.get_db), token: str = Body(), new_password: str = Body()
):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user.")
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully."}
