from enum import Enum


class StrategyType(Enum):
    CREATE_CUSTOMER = "create_customer"
    DELETE_CUSTOMER = "delete_customer"
    REMOVE_CUSTOMER = "remove_customer"

    GET_ALL = "get_all"
    GET_DETAIL = "get_detail"
    FULL_UPDATE = "full_update"
    PARTIAL_UPDATE = "partial_update"

