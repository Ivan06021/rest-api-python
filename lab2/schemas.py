from pydantic import BaseModel, field_validator, Field
from typing import Optional


class BookSchema(BaseModel):
    id: Optional[int] = Field(default=None, exclude=True)
    title: str = Field(..., min_length=3, max_length=30)
    author: str = Field(..., min_length=3, max_length=30)
    year: int = Field(..., ge=1000, le=2025)

    @field_validator("title")
    def validate_title_length(cls, v):
        if len(v) < 3 or len(v) > 30:
            raise ValueError("Довжина назви має бути від 3 до 30 символів")
        return v

    @field_validator("author")
    def validate_author_length(cls, v):
        if len(v) < 3 or len(v) > 30:
            raise ValueError("Довжина імені автора має бути від 3 до 30 символів")
        return v

    @field_validator("year")
    def validate_year_range(cls, v):
        if v < 1000 or v > 2025:
            raise ValueError("Рік має бути між 1000 та 2025")
        return v
