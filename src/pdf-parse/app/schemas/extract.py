from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel


class CoordOriginType(StrEnum):
    TOPLEFT = "TOPLEFT"
    BOTTOMLEFT = "BOTTOMLEFT"


class BoundingBox(BaseModel):
    left: float
    top: float
    right: float
    bottom: float
    coord_origin: CoordOriginType


class BaseMeta(BaseModel):
    bbox: BoundingBox


class TableRowMeta(BaseMeta):
    raw_row_idx: int
    row_section: Optional[bool] = None
    row_header: Optional[bool] = None
    column_header: Optional[bool] = None


class TableRow(BaseModel):
    meta: TableRowMeta
    data: List[str]


class TableMeta(BaseModel):
    page_number: str


class ParsedTable(BaseModel):
    meta: TableMeta
    data: List[TableRow]


class Element(BaseModel):
    text: str
    bbox: BoundingBox
    type: str  # "text", "table", "heading"


class Page(BaseModel):
    page_number: int
    text: str
    elements: list[Element]


class ExtractionResponse(BaseModel):
    pages: list[Page]
