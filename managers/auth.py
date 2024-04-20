from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import DBUser
from db.repository.auth import AuthRepository
from vendors.exception import UsernameNotUnique, RowNotFound, PasswordNotCorrect

import hashlib
from configs.config import SALT


class AuthManager:
    @classmethod
    async def register(cls, session: AsyncSession, username: str, password: str) -> DBUser:

        users: list[DBUser] = await AuthRepository(session).get_user_by_username(username=username)

        if len(users) > 0:
            raise UsernameNotUnique

        hash_object = hashlib.sha256()  # Add the salt to the password and hash it
        hash_object.update(SALT + password.encode())  # Get the hex digest of the hash
        password = hash_object.hexdigest()
        await AuthRepository(session).register_user(username=username, password=password)

        return await AuthRepository(session).get_user_by_username(username=username)

    @staticmethod
    async def login(session, username: str, password_user: str) -> DBUser:

        password = await AuthRepository(session).get_password(username=username)
        if len(password) < 1:
            raise RowNotFound
        password = password[0]
        hash_object = hashlib.sha256()  # Add the salt to the password and hash it
        hash_object.update(SALT + password_user.encode())  # Get the hex digest of the hash
        password_user = hash_object.hexdigest()

        if password != password_user:
            raise PasswordNotCorrect

        return await AuthRepository(session).get_user_by_username(username=username)
