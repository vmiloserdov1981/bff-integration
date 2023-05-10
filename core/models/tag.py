from pydantic import BaseModel, conlist
from typing import Optional


class DeadZone(BaseModel):
    type: str
    value: int


class ParamItem(BaseModel):
    value: int
    isActive: bool

    @property
    def str_value(self) -> str:
        return str(self.value)


class ThresholdItem(BaseModel):
    value: int
    # TODO: rewrite with enum
    severity: str
    isActive: bool

    @property
    def str_value(self) -> str:
        return str(self.value)


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

    @property
    def upper_active_thresholds(self) -> list[ThresholdItem]:
        return [t for t in self.thresholds.upper if t.isActive]

    @property
    def lower_active_thresholds(self) -> list[ThresholdItem]:
        return [t for t in self.thresholds.lower if t.isActive]


    @property
    def first_upper_active(self) -> ThresholdItem:
        return next((t for t in self.thresholds.upper if t.isActive), None)

    @property
    def first_lower_active(self) -> ThresholdItem:
        return next((t for t in self.thresholds.lower if t.isActive), None)


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
