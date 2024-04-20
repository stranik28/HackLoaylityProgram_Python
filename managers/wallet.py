import io

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.operations import DBOperation
from db.repository.wallet import WalletRepository

import qrcode


class WalletManager:

    @staticmethod
    async def get_wallet(session: AsyncSession, user_id: int) -> (int, list[DBOperation]):
        wallet = await WalletRepository(session).get_wallet_balance(user_id)
        operations = await WalletRepository(session).get_operations_by_user(user_id)
        wallet = wallet[0].balance
        return wallet, operations

    @staticmethod
    async def gen_qr(user_id: int) -> io.BytesIO:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f"affirmation_{user_id}")
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img_byte_array = io.BytesIO()

        img.save(img_byte_array, format='PNG')

        return img_byte_array

    @staticmethod
    async def spend_wallet_bonus(receiver_id: int, user_id: int, session: AsyncSession, amount: int):
        company = await WalletRepository(session).get_compony_employee(user_id)
        await WalletRepository(session).make_operation(amount=amount, user_id=receiver_id, company_id=company.id)
