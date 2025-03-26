from com.junyeongc.account.guest.customer.models.customer_action import StrategyType, CustomerAction
from com.junyeongc.account.guest.customer.services.create_customer_service import CreateCustomer
from com.junyeongc.account.guest.customer.services.delete_customer_service import DeleteCustomer, RemoveCustomer 
from com.junyeongc.account.guest.customer.services.get_customer_service import GetAll, GetDetail
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.services.update_customer_service import FullUpdate,  PartialUpdate


class CustomerFactory:

    strategy_map = {
        # 생성 전략
        StrategyType.CREATE_CUSTOMER: CreateCustomer(),
       
        # 조회 전략
        StrategyType.GET_ALL: GetAll(),
        StrategyType.GET_DETAIL: GetDetail(),
        
        # 업데이트 전략
        StrategyType.FULL_UPDATE: FullUpdate(),
        StrategyType.PARTIAL_UPDATE: PartialUpdate(),
        
        # 삭제 전략
        StrategyType.DELETE_CUSTOMER: DeleteCustomer(),
        StrategyType.REMOVE_CUSTOMER: RemoveCustomer(),
    }

    @staticmethod
    async def execute(
        strategy, 
        **kwargs
    ):
        # CustomerAction이나 StrategyType 모두 사용 가능하도록 처리
        if isinstance(strategy, CustomerAction):
            # CustomerAction을 StrategyType으로 변환
            strategy_value = strategy.value
            strategy = StrategyType(strategy_value)
        
        instance = CustomerFactory.strategy_map.get(strategy)
        if not instance:
            raise ValueError(f"Invalid strategy: {strategy}")
        
        if not hasattr(instance, "handle"):
            raise AttributeError(f"Strategy '{strategy}' does not have a 'handle' method.")

        # 항상 handle 메소드 호출
        return await instance.handle(**kwargs)