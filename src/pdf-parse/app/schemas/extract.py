from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel


class CoordOriginEnum(StrEnum):
    TOPLEFT = "TOPLEFT"
    BOTTOMLEFT = "BOTTOMLEFT"


class BoundingBox(BaseModel):
    left: float
    top: float
    right: float
    bottom: float
    coord_origin: CoordOriginEnum


class BaseMeta(BaseModel):
    bbox: Optional[BoundingBox] = None
    page_number: Optional[str] = None


class TableRowMeta(BaseMeta):
    raw_row_idx: int
    row_section: Optional[bool] = None
    row_header: Optional[bool] = None
    column_header: Optional[bool] = None


class TableRow(BaseModel):
    meta: TableRowMeta
    data: List[str]


class ParsedTable(BaseModel):
    meta: BaseMeta
    data: List[TableRow]


class ParseSectionHeader(BaseModel):
    meta: BaseMeta
    data: str


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
