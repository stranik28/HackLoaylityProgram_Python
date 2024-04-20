from fastapi import APIRouter, Depends
from server.depends import get_session, get_auth_account_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/wallet', tags=['wallet'])


@router.get('/')
async def get_wallet(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    return {
        "balance": 2000,
        "operations": [
            {
                "logo": "https://cdn.discordapp.com/attachments",
                "amount": 300,
                "name": "O'key store"
            },
            {
                "logo": "https://cdn.discordapp.com",
                "amount": -10,
                "name": "Beach icecream"
            }

        ]
    }
