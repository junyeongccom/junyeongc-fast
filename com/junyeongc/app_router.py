from fastapi import APIRouter
from com.junyeongc.account.guest.customer.web.customer_router import router as customer_router
from com.junyeongc.account.staff.manager.web.manager_router import router as manager_router

router = APIRouter()

router.include_router(customer_router, prefix="/customer")
router.include_router(manager_router, prefix="/manager")
