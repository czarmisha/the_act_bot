from pydantic import BaseModel, ConfigDict


class Image(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_file_path: str | None = None
    tg_file_unique_id: str | None = None
    tg_file_id: str | None = None
    product_id: int | None = None


class ImageIn(BaseModel):
    tg_file_path: str | None = None
    tg_file_unique_id: str | None = None
    tg_file_id: str | None = None
    product_id: int | None = None


class ImageOut(Image):
    id: int
