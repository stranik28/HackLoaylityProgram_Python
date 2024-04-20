import datetime
from typing import Optional

from sqlalchemy import select

from db.models.password import DBPassword
from db.models.users import DBUser
from db.repository.base import BaseRepository


class AuthRepository(BaseRepository):
    async def get_user_by_username(self, username: str) -> Optional[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                DBUser.username == username
            )
            .limit(1)
        )

        return await self.all_ones(query)

    async def get_by_id(self, account_id: int) -> Optional[DBUser]:
        query = (
            select(DBUser)
            .select_from(DBUser)
            .where(
                DBUser.id == account_id
            )
        )

        return await self.one_val(query)

    async def get_password(self, username: str) -> list[str]:

        query = (
            select(DBPassword.password)
            .select_from(DBPassword)
            .join(DBUser, DBUser.id == DBPassword.user_id, isouter=False)
            .where(
                DBUser.username == username
            )
            .limit(1)
        )

        return await self.all_ones(query)

    async def register_user(self, username: str, password: str) -> None:
        user = DBUser(username=username)

        await self.add_model(user)
        password = DBPassword(password=password, user_id=user.id)

        await self.add_model(password)
