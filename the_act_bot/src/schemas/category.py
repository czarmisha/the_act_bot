from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    brand_id: int | None = None
    position: int | None = None
    active: bool | None = None


class CategoryIn(BaseModel):
    name: str | None = None
    brand_id: int | None = None
    position: int | None = None


class CategoryOut(Category):
    id: int
