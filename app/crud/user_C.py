from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated

from ..database import get_database
from ..models.user_M import User
from ..schemas.user_S import UserCreateSchema, UserResponseSchema
from ..routes.auth_R import hash_passward, varify_passward, generate_token

router = APIRouter(
    prefix='/user',
    tags=["Authentication"]
)

@router.post(
    '/register',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def register(db:Annotated[AsyncSession,Depends(get_database)],user:UserCreateSchema):
    query = select(User).where(User.email==user.email)
    result = await db.execute(query)
    exesiting_user = result.scalar_one_or_none()
    if exesiting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )
    secure_passward = hash_passward(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        password_hash = secure_passward
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post('/login')
async def login(
    db:Annotated[AsyncSession,Depends(get_database)],
    form:Annotated[OAuth2PasswordRequestForm,Depends()]
):
    query = select(User).where(User.email == form.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user or not varify_passward(form.password,user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User account is deactivated."
        )
    access_token = generate_token(data={'sub':user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }