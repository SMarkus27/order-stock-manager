from src.api.manager.v1.exceptions import ApiException


class ProductAlreadyExists(ApiException):
    status_code = 400
    detail = "Product already exists"


class ProductNotFound(ApiException):
    status_code = 404
    detail = "Product not found"


class ProductOutOfStock(ApiException):
    status_code = 400

    def __init__(self, product_id):
        super().__init__(detail=f"Insufficient stock for product {product_id}")
