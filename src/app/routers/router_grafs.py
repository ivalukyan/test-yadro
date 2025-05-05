from fastapi import APIRouter


router = APIRouter(prefix="/api/graph")


@router.post("/")
async def create_graph():
    return {"id": 0}


@router.get("/{graph_id}")
async def read_graph(graph_id: int):
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
async def get_adjancency_list(graph_id: int):
    return {
        "adjacency_list": {
            "additionalProp1": [
                "string"
            ]
        }
    }


@router.get("/{graph_id}/reverse_adjacency_list")
async def get_adjancency_list(graph_id: int):
    return {
        "adjacency_list": {
            "additionalProp1": [
                "string"
            ]
        }
    }


@router.delete("/{graph_id}/node/{node_name}")
async def delete_node(graph_id: int, node_name: str):
    pass