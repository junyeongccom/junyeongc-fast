from fastapi import APIRouter
from com.hc_fast.account.account_router import account_router

router = APIRouter()

router.include_router(account_router, prefix="/account")
