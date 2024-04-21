from server.routers.auth import router as auth_router
from server.routers.wallet import router as wallet_router
from server.routers.wallet import ride_router

all_routers = [auth_router, wallet_router, ride_router]
