from fastapi import APIRouter, HTTPException, Depends
from backend.schemas.schemas_graph import GraphSchema, ResponseGraphSchema, ListGraphsSchema
from database.utils import UtilsAdjacencyGraphs
from database.engine import get_db_session
from sqlalchemy.orm import Session


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

    return ResponseGraphSchema(**res)


@router.get("/{graph_id}/adjacency_list")
async def get_adjancency_list(graph_id: int, session: Session = Depends(get_db_session)) -> ListGraphsSchema:
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
            detail="Adjancency graph not found"
        )

    return res


@router.get("/{graph_id}/reverse_adjacency_list")
async def get_adjancency_list(graph_id: int, session: Session = Depends(get_db_session)) -> ListGraphsSchema:
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
            detail="Adjancency graph not found"
        )

    return res


@router.delete("/{graph_id}/node/{node_name}")
async def delete_node(graph_id: int, node_name: str, session: Session = Depends(get_db_session)):
    if graph_id < 0:
        raise HTTPException(
            status_code=422,
            detail="Validation Error"
        )
    
    adj_graph = UtilsAdjacencyGraphs(session)
    await adj_graph.delete_graph(graph_id, node_name)
