




from com.junyeongc.auth.user.service.hello_user import HelloUser


strategy_map = {
    "hello_user": HelloUser(),
}

class UserFactory:
    @staticmethod
    def create(strategy, **kwargs):
        instance = strategy_map[strategy]
        if not instance:
            raise Exception("Invalid strategy")
        return instance.handle(**kwargs)