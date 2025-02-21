import hashlib
import random
import string
import uuid
from typing import Annotated, Optional, Union

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy import insert, delete, select, or_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.core.auth import get_current_user
from app.core.schemas import User, UserChange, UserCheck
from app.core.db import db_session
from app.core.security import verify_password, get_hashed_password
from app.models import Users, UsersProject2
from app.services.m_email_service import ClassEmail

router = APIRouter()


@router.post(
    path='/check_user',
    response_model=UserCheck,
    status_code=HTTP_200_OK,
    summary='Check user in DB.',
)
async def check_user(
        user: UserCheck,
        # _: Annotated[Users, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),

):
    async with db_session:
        stmt = select(Users).filter(Users.email == user.email)
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

    if not user_in_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'User not found in DB.',
        )

    try:
        if verify_password(password=user.password, hashed_pass=user_in_db[0].password):
            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly checked: {user}',
            )
        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User password incorrect.',
            )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Error: {e}',
        )


@router.post(
    path='/reset_password',
    status_code=HTTP_200_OK,
    summary='Reset password user in DB by confirmation code to email.',
)
async def reset_password(
        email: EmailStr,
        # _: Annotated[Users, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),

):
    async with db_session:
        stmt = select(Users).filter(Users.email == email)
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

    if not user_in_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'User not found in DB.',
        )

    code: str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    result = ClassEmail.send_text(text=code, to=email)


    if result:
        async with db_session:
            stmt = update(Users).where(Users.email == email).values(confiramtion_code=code)
            await db_session.execute(statement=stmt)
            await db_session.commit()

        return JSONResponse(
            status_code=HTTP_200_OK,
            content=f'Password successfuly reseted for: {email}',
        )
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Error: {result}',
        )

@router.post(
    path='/check_code',
    status_code=HTTP_200_OK,
    summary='Check user in DB.',
)
async def check_code(
        email: EmailStr,
        code: str,
        # _: Annotated[Users, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),

):
    async with db_session:
        stmt = select(Users).filter(Users.email == email)
        result = await db_session.execute(statement=stmt)
        user_in_db: User = result.one_or_none()

    if not user_in_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'User not found in DB.',
        )
    


    try:
        if code == user_in_db[0].confiramtion_code:

            async with db_session:
                stmt = update(Users).where(Users.email == email).values(confiramtion_code=None)
                await db_session.execute(statement=stmt)
                await db_session.commit()

            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly checked: {email}',

            )

        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'Confiramtion_code incorrect.',
            )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Error: {e}',
        )

@router.post(
    path='/create_user',
    response_model=User,
    status_code=HTTP_200_OK,
    summary='Add new user',
)
async def create_user(
        user: User,
        # _: Annotated[Users, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),

):
    async with db_session:
        stmt = select(Users).filter(or_(Users.login == user.login, Users.email == user.email))
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User already created.',
            )
        else:
            stmt = insert(Users).values(
                login=user.login,
                password=user.password,
                email=user.email
            )
            await db_session.execute(statement=stmt)
            await db_session.commit()

            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly created: {user}',
            )


@router.patch(
    path='/update_user',
    summary='Change user',
    response_model=UserChange,
    status_code=HTTP_200_OK,
)
async def update_user(
        user: UserChange,
        login: str = None,
        email: str = None,
        # _: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),
):
    if not (login or email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Must fill login or email field.',
        )

    async with db_session:
        stmt = select(Users).filter(or_(Users.login == login, Users.email == email))
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

    if not user_in_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'User not found in DB.',
        )

    try:
        stmt = update(Users).where(or_(Users.login == login, Users.email == email)).values(
            user.model_dump(exclude_unset=True))
        await db_session.execute(statement=stmt)
        await db_session.commit()

        return JSONResponse(
            status_code=HTTP_200_OK,
            content=f'User successfuly changed: {user}',
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Error: {e}',
        )






@router.delete(
    path='/delete',
    status_code=HTTP_200_OK,
    summary='Delete user',
)
async def delete_user(
        login: str,
        # _: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(db_session),
):
    async with db_session:
        stmt = select(Users).where(Users.login == login)
        result = await db_session.execute(statement=stmt)
        user_in_db = result.one_or_none()

        if user_in_db:
            stmt = delete(Users).where(Users.login == login)
            await db_session.execute(statement=stmt)
            await db_session.commit()

            return JSONResponse(
                status_code=HTTP_200_OK,
                content=f'User successfuly deleted: {login}',
            )

        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'User not found in DB.',
            )
