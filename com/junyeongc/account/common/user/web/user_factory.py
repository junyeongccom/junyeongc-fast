strategy_map = 1

class UserFactory:
    @staticmethod
    def create(strategy, **kwargs):
        instance = strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)