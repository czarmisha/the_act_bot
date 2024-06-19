from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: dict | None = None
    stock: int = 0
    price: int


class ProductIn(BaseModel):
    name: str | None = None
    description: dict | None = None
    stock: int = 0
    price: int


class ProductOut(Product):
    id: int
