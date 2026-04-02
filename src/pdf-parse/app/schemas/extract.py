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


class GroupTypeEnum(StrEnum):
    KVArea = "key_value_area"
    List = "list"


class KVGroup(BaseModel):
    type: GroupTypeEnum = GroupTypeEnum.KVArea
    data: dict[str, str]


class ListGroup(BaseModel):
    type: GroupTypeEnum = GroupTypeEnum.List
    data: list[str]


class ParsedGroups(BaseModel):
    meta: BaseMeta
    data: list[KVGroup | ListGroup]


class Element(BaseModel):
    text: str
    bbox: BoundingBox
    type: str  # "text", "table", "heading"


class PageSize(BaseModel):
    width: float
    height: float


class PageMeta(BaseMeta):
    size: PageSize


class Page(BaseModel):
    meta: PageMeta
    section_headers: Optional[list[ParseSectionHeader]] = None
    groups: Optional[ParsedGroups] = None
    tables: Optional[list[ParsedTable]] = None


ExtractionResponse = dict[str, Page]
