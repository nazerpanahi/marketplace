from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.product import router as product_router
from .endpoints.category import router as category_router
from .endpoints.user import router as user_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(product_router, prefix='/products', tags=['products'])
router.include_router(category_router, prefix='/categories', tags=['categories'])
router.include_router(user_router, prefix='/user', tags=['user'])
