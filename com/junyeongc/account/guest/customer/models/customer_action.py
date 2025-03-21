from enum import Enum


class StrategyType(Enum):
    CREATE_CUSTOMER = "create_customer"
    DELETE_CUSTOMER = "delete_customer"
    REMOVE_CUSTOMER = "remove_customer"

    GET_ALL = "get_all"
    GET_DETAIL = "get_detail"
    FULL_UPDATE = "full_update"
    PARTIAL_UPDATE = "partial_update"


# CustomerAction은 StrategyType과 동일한 값을 가지는 별칭 역할을 합니다
class CustomerAction(Enum):
    CREATE_CUSTOMER = "create_customer"
    DELETE_CUSTOMER = "delete_customer"
    REMOVE_CUSTOMER = "remove_customer"

    GET_ALL = "get_all"
    GET_DETAIL = "get_detail"
    FULL_UPDATE = "full_update"
    PARTIAL_UPDATE = "partial_update"

