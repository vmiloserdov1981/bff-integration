from pydantic import BaseModel
from typing import Optional


class UnitNode(BaseModel):
    id: Optional[int]
    name: str = ''
    nodeKind: Optional[str]
    typeId: Optional[int]
    markId: Optional[int]
    parentId: Optional[int]
    hasDegradation: Optional[bool]
    lTagCount: Optional[int]
    childrenIds: Optional[list[int]]

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)
    
    @property
    def body_for_root_creation(self) -> dict:
        return {
            'rootNode': {
                'name': self.name,
                'markId': self.markId,
                'typeId': self.typeId
            }
        }


class CreateUnitNodeResponse(BaseModel):
    result: UnitNode

    @property
    def node(self) -> UnitNode:
        return self.result


class RootUnitNode(BaseModel):
    rootNode: UnitNode


class CreateRootUnitNodeResponse(BaseModel):
    result: RootUnitNode

    @property
    def node(self) -> UnitNode:
        return self.result.rootNode


class UnitNodes(BaseModel):
    nodes: dict[str, UnitNode]
    rootId: int


class UnitNodesResponse(BaseModel):
    result: UnitNodes

    @property
    def nodes(self) -> dict[str, UnitNode]:
        return self.result.nodes
