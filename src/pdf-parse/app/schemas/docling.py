from typing import Union

from docling_core.types.doc.document import (
    CodeItem,
    FieldHeadingItem,
    FieldValueItem,
    FormulaItem,
    GroupItem,
    InlineGroup,
    ListGroup,
    ListItem,
    SectionHeaderItem,
    TextItem,
    TitleItem,
)

DoclingTexts = list[
    Union[
        TitleItem,
        SectionHeaderItem,
        ListItem,
        CodeItem,
        FormulaItem,
        FieldHeadingItem,
        FieldValueItem,
        TextItem,
    ]
]

DoclingGroups = list[Union[ListGroup, InlineGroup, GroupItem]]
