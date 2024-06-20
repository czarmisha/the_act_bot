from pydantic import BaseModel, ConfigDict


class Image(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str | None = None
    file_unique_id: str | None = None
    product_id: int | None = None


class ImageIn(BaseModel):
    url: str | None = None
    file_unique_id: str | None = None
    product_id: int | None = None


class ImageOut(Image):
    id: int
