from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from user.models.user import User
from user.schemas.user import UserOut
from user.schemas.user import UserCreate
from auth.utils.auth_utils import (get_password_hash, verify_password)
from auth.services.auth_service import create_access_token, get_current_user

from typing import Annotated
from auth.models.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.services.auth_service import authenticate_user, create_access_token
from core.database import get_db

router = APIRouter(prefix="/auth", tags=['Auth'])

@router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(
        email = data.email,
        password = get_password_hash(data.password),
        role = data.role or "staff"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserOut)
def handle_me(current_user: User = Depends(get_current_user)):
    return current_user