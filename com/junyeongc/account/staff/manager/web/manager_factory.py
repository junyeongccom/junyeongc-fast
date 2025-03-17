from com.junyeongc.account.staff.manager.strategy.create_strategy import DefaultCreateStrategy, ValidatedCreateStrategy
from com.junyeongc.account.staff.manager.strategy.delete_strategy import HardDeleteStrategy, SoftDeleteStrategy
from com.junyeongc.account.staff.manager.strategy.retrieve_strategy import GetAllStrategy, GetDetailStrategy
from com.junyeongc.account.staff.manager.strategy.update_strategy import FullUpdateStrategy, PartialUpdateStrategy
from com.junyeongc.account.staff.manager.strategy.strategy_type import StrategyType
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession

class ManagerFactory:

    strategy_map = {
        StrategyType.DEFAULT_CREATE: DefaultCreateStrategy(),
        StrategyType.VALIDATED_CREATE: ValidatedCreateStrategy(),
        StrategyType.GET_ALL: GetAllStrategy(),
        StrategyType.GET_DETAIL: GetDetailStrategy(),
        StrategyType.FULL_UPDATE: FullUpdateStrategy(),
        StrategyType.PARTIAL_UPDATE: PartialUpdateStrategy(),
        StrategyType.SOFT_DELETE: SoftDeleteStrategy(),
        StrategyType.HARD_DELETE: HardDeleteStrategy(),
    }

    @staticmethod
    async def execute(
        strategy: StrategyType, 
        method: Literal["create", "retrieve", "update", "delete"], 
        db: AsyncSession,
        **kwargs
    ):
        instance = ManagerFactory.strategy_map.get(strategy)
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

