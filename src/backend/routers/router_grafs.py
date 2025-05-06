from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.backend.schemas.schemas_graph import GraphSchema, ResponseGraphSchema, ListGraphsSchema
from src.database.utils import UtilsAdjacencyGraphs
from src.database.engine import get_db_session


router = APIRouter(prefix="/api/graph")


@router.post("/")
async def create_graph(graph: GraphSchema, session: Session = Depends(get_db_session)):
    if not graph:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )
    try:
        adj_graf = UtilsAdjacencyGraphs(session)
        new_graph_id = await adj_graf.add_graph(nodes=graph.nodes, edges=graph.edges)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Failed add graph"
        )

    return {"id": new_graph_id}


@router.get("/{graph_id}")
async def read_graph(graph_id: int, session: Session = Depends(get_db_session)) -> ResponseGraphSchema:
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    adj_graph = UtilsAdjacencyGraphs(session)
    res = await adj_graph.get_graph(graph_id)

    if not res:
        raise HTTPException(
            status_code=404,
            detail="Graph not found"
        )

    return ResponseGraphSchema(graph_id=res.id, graph=GraphSchema(nodes=res.nodes, edges=res.edges))


@router.get("/{graph_id}/adjacency_list")
async def get_adjacency_list(graph_id: int, session: Session = Depends(get_db_session)) -> ListGraphsSchema:
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    adj_graph = UtilsAdjacencyGraphs(session)
    res = await adj_graph.get_adjacency_graph(graph_id)

    if not res:
        raise HTTPException(
            status_code=404,
            detail="Adjacency graph not found"
        )

    return res


@router.get("/{graph_id}/reverse_adjacency_list")
async def get_adjacency_list(graph_id: int, session: Session = Depends(get_db_session)) -> ListGraphsSchema:
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    adj_graph = UtilsAdjacencyGraphs(session)
    res = await adj_graph.get_reverse_adjacency_graph(graph_id)

    if not res:
        raise HTTPException(
            status_code=404,
            detail="Adjacency graph not found"
        )

    return res


@router.delete("/{graph_id}/node/{node_name}", status_code=204)
async def delete_node(graph_id: int, node_name: str, session: Session = Depends(get_db_session)):
    if graph_id < 0 or not node_name:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )

    adj_graph = UtilsAdjacencyGraphs(session)
    await adj_graph.delete_graph(graph_id, node_name)
