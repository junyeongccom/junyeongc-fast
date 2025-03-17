from com.junyeongc.account.guest.customer.models.customer_action import StrategyType
from com.junyeongc.account.guest.customer.services.create_customer_service import DefaultCreateStrategy
from com.junyeongc.account.guest.customer.services.delete_customer_service import DeleteCustomer, RemoveCustomer 
from com.junyeongc.account.guest.customer.services.get_customer_service import GetAll, GetDetail
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.services.update_customer_service import FullUpdate,  PartialUpdate


class CustomerFactory:

    strategy_map = {
        # 생성 전략
        StrategyType.CREATE_CUSTOMER: DefaultCreateStrategy(),
       
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
        strategy: StrategyType, 
        method: Literal["create", "retrieve", "update", "delete"], 
        db: AsyncSession,
        **kwargs
    ):
        instance = CustomerFactory.strategy_map.get(strategy)
        if not instance:
            raise ValueError(f"Invalid strategy: {strategy}")
        
        if not hasattr(instance, method):
            raise AttributeError(f"Strategy '{strategy}' does not have a '{method}' method.")

        method_to_call = getattr(instance, method)

        # 비동기 메서드 여부 확인 후 실행
        if callable(method_to_call):
            if method == "retrieve":  # retrieve는 비동기 실행
                return await method_to_call(db=db, **kwargs)
            else:
                return await method_to_call(db=db, **kwargs)
        else:
            raise TypeError(f"Method '{method}' is not callable.")

    # 고객 관련 메서드들
    @staticmethod
    def create_customer(strategy: str):
        return StrategyType.CREATE_CUSTOMER
        
    @staticmethod
    def get_customer_detail(strategy: str):
        return StrategyType.GET_DETAIL
        
    @staticmethod
    def get_customer_list(strategy: str):
        return StrategyType.GET_ALL
        
    @staticmethod
    def update_customer(strategy: str):
        return StrategyType.FULL_UPDATE
        
    @staticmethod
    def delete_customer(strategy: str):
        return StrategyType.DELETE_CUSTOMER
