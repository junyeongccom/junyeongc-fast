from com.junyeongc.account.guest.customer.models.customer_action import CustomerAction
from com.junyeongc.account.guest.customer.api.customer_factory import CustomerFactory


class CustomerController:
    
    def __init__(self):
        pass

    async def create_customer(self, db=None, **kwargs):
        print("🎃🎃 customer controller create_customer 진입함", kwargs)
        kwargs['db'] = db
        return await CustomerFactory.execute(strategy=CustomerAction.CREATE_CUSTOMER, **kwargs)

    async def get_customer_detail(self, db=None, **kwargs):
        kwargs['db'] = db
        return await CustomerFactory.execute(strategy=CustomerAction.GET_DETAIL, **kwargs)

    async def get_customer_list(self, db=None, **kwargs):
        print("🐣🐣 customer controller get_customer_list 로 진입함")
        kwargs['db'] = db
        return await CustomerFactory.execute(strategy=CustomerAction.GET_ALL, **kwargs)

    async def update_customer(self, db=None, **kwargs):
        kwargs['db'] = db
        return await CustomerFactory.execute(strategy=CustomerAction.FULL_UPDATE, **kwargs)

    async def delete_customer(self, db=None, **kwargs):
        kwargs['db'] = db
        return await CustomerFactory.execute(strategy=CustomerAction.DELETE_CUSTOMER, **kwargs)
