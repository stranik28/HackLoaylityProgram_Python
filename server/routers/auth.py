from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.request.auth import RequestRegistration
from api.response.auth import ResponseAuthFactory, ResponseUser
from db.models.users import DBUser

from managers.auth import AuthManager

from server.depends import get_session

from vendors.exception import RowNotFound, PasswordNotCorrect, UsernameNotUnique

router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post('/registration', status_code=202, response_model=ResponseUser)
async def verification_code(
        registration_data: RequestRegistration,
        session: AsyncSession = Depends(get_session)
):
    try:
        user = await AuthManager.register(session=session, username=registration_data.username,
                                          password=registration_data.password)
    except UsernameNotUnique:
        user: DBUser = await AuthManager.login(session=session, username=registration_data.username,
                                               password_user=registration_data.password)
    return ResponseAuthFactory.get_user(user=user)


@router.post('/login', response_model=ResponseUser)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    try:
        user: DBUser = await AuthManager.login(session=session, username=form_data.username,
                                               password_user=form_data.password)
    except RowNotFound:
        raise HTTPException(status_code=404, detail="Пользователя с таким username нет в системе")
    except PasswordNotCorrect:
        raise HTTPException(status_code=400, detail="Не верная связка username/пароль")
    return ResponseAuthFactory.get_user(user=user)
