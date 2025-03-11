from com.junyeongc.account.guest.customer.web.customer_factory import CustomerFactory


class CustomerController:
    
    def __init__(self):
        pass

    async def create_customer(self, **kwargs):
        return CustomerFactory.create_customer(strategy="create_customer")

    async def get_customer_detail(self, **kwargs):
        return CustomerFactory.get_customer_detail(strategy="get_customer_detail")

    async def get_customer_list(self, **kwargs):
        return CustomerFactory.get_customer_list(strategy="get_customer_list")

    async def update_customer(self, **kwargs):
        return CustomerFactory.update_customer(strategy="update_customer")

    async def delete_customer(self, **kwargs):
        return CustomerFactory.delete_customer(strategy="delete_customer")
