import uuid

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post('/login')
async def get_login(
        reusable_oauth2: OAuth2PasswordRequestForm = Depends()
):
    if reusable_oauth2.username != 'api':
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid username.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if not verify_password(plain_password=reusable_oauth2.password, hashed_password=settings.HASH):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid password.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return {"access_token": str(uuid.uuid4()), "token_type": "bearer"}



