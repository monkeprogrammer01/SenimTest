from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from core.database import get_db
from user.models.user import User
from user.schemas.user import UserOut
from user.schemas.user import UserCreate
from auth.utils.auth_utils import (get_password_hash, verify_password)
from auth.services.auth_service import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=['Auth'])

@router.post("/register", response_model=UserOut)
def handle_register(data: UserCreate, db: Session = Depends(get_db)):
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


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=60*24)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def handle_me(current_user: User = Depends(get_current_user)):
    return current_user