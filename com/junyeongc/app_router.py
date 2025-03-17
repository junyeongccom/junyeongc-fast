from fastapi import APIRouter
from com.junyeongc.account.account_router import account_router


router = APIRouter()

router.include_router(account_router)

