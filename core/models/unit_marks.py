from pydantic import BaseModel
from typing import Optional


class UnitMark(BaseModel):
    id: Optional[int]
    name: str = ''
    typeId: Optional[int]
    unitId: Optional[int]

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)


class UnitMarkListItem(BaseModel):
    id: int
    name: str = ''
    typeId: int
    unitId: Optional[int]

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)


class CreateUnitMarkResponse(BaseModel):
    result: UnitMark

    @property
    def unit_mark(self) -> UnitMark:
        return self.result


class UnitMarksListResponse(BaseModel):
    result: list[UnitMarkListItem]

    @property
    def list(self):
        return self.result
