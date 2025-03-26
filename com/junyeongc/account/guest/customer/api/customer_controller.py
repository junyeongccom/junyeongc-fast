from com.junyeongc.account.guest.customer.models.customer_action import CustomerAction
from com.junyeongc.account.guest.customer.api.customer_factory import CustomerFactory


class CustomerController:
    
    def __init__(self):
        pass

    async def create_customer(self, **kwargs):
        print("🎃🎃 customer controller create_customer 진입함", kwargs)
        return await CustomerFactory.execute(strategy=CustomerAction.CREATE_CUSTOMER, **kwargs)

    async def get_customer_detail(self, **kwargs):
        return await CustomerFactory.execute(strategy=CustomerAction.GET_DETAIL, **kwargs)

    async def get_customer_list(self, **kwargs):
        print("🐣🐣 customer controller get_customer_list 로 진입함")
        return await CustomerFactory.execute(strategy=CustomerAction.GET_ALL, **kwargs)

    async def update_customer(self, **kwargs):
        return await CustomerFactory.execute(strategy=CustomerAction.FULL_UPDATE, **kwargs)

    async def delete_customer(self, **kwargs):
        return await CustomerFactory.execute(strategy=CustomerAction.DELETE_CUSTOMER, **kwargs)
