from fastapi import APIRouter, HTTPException
from backend.schemas.schemas_graph import GraphSchema, ResponseGraphSchema, ListGraphsSchema


router = APIRouter(prefix="/api/graph")


@router.post("/")
async def create_graph(graph: GraphSchema):
    if not graph:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    return {"id": 0}


@router.get("/{graph_id}")
async def read_graph(graph_id: int) -> ResponseGraphSchema:
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    return {
        "id": graph_id,
        "nodes": [
            {
            "name": ""
            }
        ],
        "edges": [
            {
            "source": "",
            "target": ""
            }
        ]
    }


@router.get("/{graph_id}/adjacency_list")
async def get_adjancency_list(graph_id: int) -> ListGraphsSchema:
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    return {
        "adjacency_list": {
            "additionalProp1": [
                "string"
            ]
        }
    }


@router.get("/{graph_id}/reverse_adjacency_list")
async def get_adjancency_list(graph_id: int) -> ListGraphsSchema:
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    return {
        "adjacency_list": {
            "additionalProp1": [
                "string"
            ]
        }
    }


@router.delete("/{graph_id}/node/{node_name}")
async def delete_node(graph_id: int, node_name: str):
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )
    pass