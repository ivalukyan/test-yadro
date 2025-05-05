from pydantic import BaseModel
from typing import List, Dict


class GraphSchema(BaseModel):
    nodes: List[Dict[str, str]]
    edges: List[Dict[str, str]]


class ResponseGraphSchema(BaseModel):
    graph_id: int
    graph: GraphSchema


class ListGraphsSchema(BaseModel):
    adjacency_list: Dict[str, List[str]]

