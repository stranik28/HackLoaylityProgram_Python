from fastapi import APIRouter, Depends, Response

from api.response.wallet import WalletResponseFactory, WalletResponse
from managers.wallet import WalletManager
from server.depends import get_session, get_auth_account_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/wallet', tags=['wallet'])
ride_router = APIRouter(prefix="ride", tags=["ride"])


@router.get('/', response_model=WalletResponse)
async def get_wallet(
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)
):
    balance, operations = await WalletManager.get_wallet(session=session, user_id=user_id)
    return WalletResponseFactory.get_from_models(balance, operations)


@router.get('/gen_qr')
async def get_wallet_qr(
        user_id: int = Depends(get_auth_account_id)
):
    response = await WalletManager.gen_qr(user_id)
    return Response(content=response.getvalue(), media_type="image/png")


@router.post('/send_bonus', status_code=200)
async def send_wallet_bonus(
        receiver_id: int,
        amount: int,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)

):
    await WalletManager.spend_wallet_bonus(receiver_id=receiver_id, user_id=user_id, session=session, amount=amount)


@router.post('/spend_bonus', status_code=200)
async def spend_wallet_bonus(
        receiver_id: int,
        amount: int,
        user_id: int = Depends(get_auth_account_id),
        session: AsyncSession = Depends(get_session)

):
    await WalletManager.spend_wallet_bonus(receiver_id=receiver_id, user_id=user_id, session=session, amount=-amount)


@ride_router.get('/touch_esp/{esp_id}/{uuid}', status_code=200)
async def touch(
        uuid: str,
        esp_id: int,
        session: AsyncSession = Depends(get_session)
):
    print(f"Ought uuid is {uuid} from esp {esp_id}")
    return {"result": uuid}
