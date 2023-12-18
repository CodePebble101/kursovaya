from app.endpoints.register import register_router
from app.endpoints.tFA import tfa_router

all_routes = [
    register_router,
    tfa_router
]

__all__ = [
    'all_routes'
]
