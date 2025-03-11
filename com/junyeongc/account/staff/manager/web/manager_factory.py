

class ManagerFactory:


    @staticmethod
    def create_manager(strategy, **kwargs):
        instance = ManagerFactory.strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)

    @staticmethod
    def get_manager_detail(strategy, **kwargs):
        instance = ManagerFactory.strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)
    
    @staticmethod
    def get_manager_list(strategy, **kwargs):
        instance = ManagerFactory.strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)

    @staticmethod
    def update_manager(strategy, **kwargs):
        instance = ManagerFactory.strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)
    
    @staticmethod
    def delete_manager(strategy, **kwargs):
        instance = ManagerFactory.strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)
    
