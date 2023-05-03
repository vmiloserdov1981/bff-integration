from pydantic import BaseModel, conlist
from typing import Optional


class DeadZone(BaseModel):
    type: str
    value: int


class ParamItem(BaseModel):
    value: int
    isActive: bool


class ThresholdItem(BaseModel):
    value: int
    # TODO: rewrite with enum
    severity: str
    isActive: bool


class Thresholds(BaseModel):
    upper: list[ThresholdItem]
    lower: list[ThresholdItem]


class ParamRange(BaseModel):
    upper: ParamItem
    lower: ParamItem


class NamedValue(BaseModel):
    displayName: str
    value: int


class Tag(BaseModel):
    uuid: Optional[str]
    title: Optional[str]
    value: int = 0
    # TODO: rewrite with enum
    physicalQuantity: str
    # TODO: rewrite with enum
    physicalQuantityUnit: str
    markedAsObservable: bool = False
    deadZone: DeadZone
    thresholds: Thresholds
    operatingRange: ParamRange
    displayRange: ParamRange
    unitId: int = 0
    namedValues: list[NamedValue]

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)


class CreateTagResponse(BaseModel):
    result: Tag

    @property
    def tag(self) -> Tag:
        return self.result


class TagsResponse(BaseModel):
    result: conlist(Tag, min_items=0)
    
    @property
    def list(self) -> list[Tag]:
        return self.result
