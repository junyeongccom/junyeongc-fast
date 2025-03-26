from fastapi import APIRouter
from com.junyeongc.account.auth.user.api.user_router import router as user_router

account_router = APIRouter()

account_router.include_router(user_router, prefix="/user")