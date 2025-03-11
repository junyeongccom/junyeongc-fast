from com.junyeongc.account.staff.manager.web.manager_factory import ManagerFactory


class ManagerController:
    
    def __init__(self):
        pass

    def create_manager(self, **kwargs):
        return ManagerFactory.create_manager(strategy="create_manager")

    def get_manager_detail(self, **kwargs):
        return ManagerFactory.get_manager_detail(strategy="get_manager_detail")

    def get_manager_list(self, **kwargs):
        return ManagerFactory.get_manager_list(strategy="get_manager_list")

    def update_manager(self, **kwargs):
        return ManagerFactory.update_manager(strategy="update_manager")

    def delete_manager(self, **kwargs):
        return ManagerFactory.delete_manager(strategy="delete_manager")
