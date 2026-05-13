from src.api.manager.v1.exceptions import ApiException


class EmptyOrder(ApiException):
    status_code = 400
    detail = "Order must have at least one item"
