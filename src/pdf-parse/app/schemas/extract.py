from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float


class Element(BaseModel):
    text: str
    bbox: BoundingBox
    type: str  # "text", "table", "heading"


class Page(BaseModel):
    page_number: int
    text: str
    elements: list[Element]


class Table(BaseModel):
    page_number: int
    rows: list[list[str]]
    bbox: BoundingBox


class ExtractionResponse(BaseModel):
    pages: list[Page]
    tables: list[Table]
