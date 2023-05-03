from pydantic import BaseModel
from typing import Optional, Union


class CommonNode(BaseModel):
    id: Optional[int]
    name: str = ''
    typeId: Optional[int]
    treeRootId: Optional[int]
    parentId: Optional[int]
    childrenIds: Optional[list[int]]
    unitNodeTreeRootIdRef: Optional[int]

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)


class RootElem(BaseModel):
    rootElem: CommonNode

    @property
    def body_for_creation(self) -> dict:
        return self.dict(exclude_unset=True)

    @property
    def body_for_update(self) -> dict:
        return self.node.dict(exclude_unset=True)

    @property
    def node(self) -> CommonNode:
        return self.rootElem


class RootNodeResponse(BaseModel):
    result: RootElem


class NodeResponse(BaseModel):
    result: CommonNode


class RootNodesList(BaseModel):
    result: list[RootElem]


class ChildNode(BaseModel):
    id: int
    name: str
    childrenIds: list[int]


class AttachedNode(BaseModel):
    id: int
    isVisible: Optional[bool]
    name: str
    parentId: str
    status: Optional[str]
    statusDisplay: Optional[str]
    unitId: int


class AttachNodeResponse(BaseModel):
    result: AttachedNode

    @property
    def node(self) -> AttachedNode:
        return self.result


class TreeResponse(BaseModel):
    rootId: int
    nodes: dict[str, Union[CommonNode, AttachedNode]]


class TreeResponseResult(BaseModel):
    result: TreeResponse

    @property
    def nodes(self) -> dict[str, Union[CommonNode, AttachedNode]]:
        return self.result.nodes
