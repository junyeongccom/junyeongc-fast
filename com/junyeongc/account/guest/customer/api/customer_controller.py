from com.junyeongc.account.guest.customer.api.customer_factory import CustomerFactory
from com.junyeongc.account.guest.customer.models.customer_action import StrategyType


class CustomerController:
    
    def __init__(self):
        pass

    async def create_customer(self, db=None, **kwargs):
        if db:
            return await CustomerFactory.execute(
                strategy=StrategyType.CREATE_CUSTOMER, 
                method="create", 
                db=db, 
                **kwargs
            )
        return CustomerFactory.create_customer(strategy="create_customer")

    async def get_customer_detail(self, db=None, **kwargs):
        if db:
            return await CustomerFactory.execute(
                strategy=StrategyType.GET_DETAIL, 
                method="retrieve", 
                db=db, 
                **kwargs
            )
        return CustomerFactory.get_customer_detail(strategy="get_detail_customer")

    async def get_customer_list(self, db, **kwargs):
        return await CustomerFactory.execute(
            strategy=StrategyType.GET_ALL, 
            method="retrieve", 
            db=db, 
            **kwargs
        )

    async def update_customer(self, db=None, **kwargs):
        if db:
            return await CustomerFactory.execute(
                strategy=StrategyType.FULL_UPDATE, 
                method="update", 
                db=db, 
                **kwargs
            )
        return CustomerFactory.update_customer(strategy="update_customer")

    async def delete_customer(self, db=None, **kwargs):
        if db:
            return await CustomerFactory.execute(
                strategy=StrategyType.DELETE_CUSTOMER, 
                method="delete", 
                db=db, 
                **kwargs
            )
        return CustomerFactory.delete_customer(strategy="delete_customer")
