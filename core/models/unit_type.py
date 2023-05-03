from pydantic import BaseModel
from typing import Optional


class UnitType(BaseModel):
    id: Optional[int]
    name: str = ''

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)


class CreateUnitTypeResponse(BaseModel):
    result: UnitType

    @property
    def unit_type(self) -> UnitType:
        return self.result


class UnitTypesListResponse(BaseModel):
    result: list[UnitType]
