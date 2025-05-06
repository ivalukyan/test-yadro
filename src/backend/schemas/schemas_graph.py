from pydantic import BaseModel
from typing import List, Dict


class NodeSchema(BaseModel):
    name: str


class EdgeSchema(BaseModel):
    source: str
    target: str


class GraphSchema(BaseModel):
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]


class ResponseGraphSchema(BaseModel):
    graph_id: int
    graph: GraphSchema

    class Config:
        from_orm = True


class ListGraphsSchema(BaseModel):
    adjacency_list: Dict[str, List[str]]

    class Config:
        from_attributes = True
        from_orm = True

