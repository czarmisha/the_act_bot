from pydantic import BaseModel, ConfigDict


class Brand(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    position: int | None = None
    active: bool | None = None


class BrandIn(BaseModel):
    name: str | None = None
    position: int | None = None


class BrandOut(Brand):
    id: int
