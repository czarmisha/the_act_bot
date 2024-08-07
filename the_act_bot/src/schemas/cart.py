from pydantic import BaseModel, ConfigDict


class CartItem(BaseModel):
    product_id: int
    quantity: int


class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int | None = None
    items: list[CartItem] | None = None


class CartIn(Cart):
    pass


class CartOut(Cart):
    id: int


class AddCartItem(BaseModel):
    product_id: int
    quantity: int
