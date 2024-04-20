from server.routers.auth import router as auth_router
from server.routers.wallet import router as wallet_router

all_routers = [auth_router, wallet_router]
