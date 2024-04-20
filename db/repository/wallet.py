from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from db.models.company import DBCompany
from db.models.operations import DBOperation
from db.models.wallet import DBWallet
from db.models.users import DBUser
from db.repository.base import BaseRepository
from vendors.exception import NegativeBalanceException


class WalletRepository(BaseRepository):

    async def get_wallet_balance(self, user_id: int) -> list[DBWallet]:
        query = (
            select(DBWallet)
            .select_from(DBWallet)
            .where(DBWallet.user_id == user_id)
            .limit(1)
        )
        return await self.all_ones(query)

    async def get_operations_by_user(self, user_id: int) -> list[DBOperation]:
        query = (
            select(DBOperation)
            .select_from(DBOperation)
            .where(DBOperation.user_id == user_id)
            .order_by(desc(DBOperation.created_at))
        )
        query = query.options(
            joinedload(DBOperation.company)
        )
        return await self.all_ones(query)

    async def create_wallet(self, user_id: int):
        wallet = DBWallet(user_id=user_id, balance=600)
        await self.add_model(wallet)

    async def get_compony_employee(self, user_id: int) -> DBCompany:
        query = (
            select(DBUser.employer_id)
            .select_from(DBUser)
            .where(DBUser.id == user_id)
            .limit(1)
        )

        user = await self.all_ones(query)
        user = user[0]
        query = (
            select(DBCompany)
            .select_from(DBCompany)
            .where(DBCompany.id == user)
            .limit(1)
        )
        company = await self.all_ones(query)
        company = company[0]
        return company

    async def prepare_transaction(self, amount: int, user_id: int):
        query = (
            select(DBWallet)
            .select_from(DBWallet)
            .where(DBWallet.user_id == user_id)
            .limit(1)
        )
        wallet = await self.all_ones(query)
        wallet = wallet[0]
        if wallet.balance + amount < 0:
            raise NegativeBalanceException

        wallet.balance += amount
        await self._session.commit()

    async def make_operation(self, amount: int, user_id: int, company_id: int):
        await self.prepare_transaction(amount, user_id)
        transaction = DBOperation(
            amount=amount,
            user_id=user_id,
            company_id=company_id
        )
        await self.add_model(transaction)

