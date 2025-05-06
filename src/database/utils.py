from fastapi import HTTPException

from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

from database.models import AdjacencyGraphs, NodesGraphs, EdgesGraphs
from backend.schemas.schemas_graph import ListGraphsSchema


class UtilsAdjacencyGraphs():
    def __init__(self, db_session: Session):
        self.session = db_session

    async def add_graph(self, nodes: List[NodesGraphs], edges: List[EdgesGraphs]) -> int:
        async for db_session in self.session:
            try:
                new_graph = AdjacencyGraphs(nodes=nodes, edges=edges)
                db_session.add(new_graph)
                await db_session.commit()
                await db_session.refresh(new_graph)
                return new_graph.id
            except Exception as e:
                await db_session.rollback()
                raise e
    

    async def get_graph(self, graph_id: int) -> AdjacencyGraphs:
        async for db_session in self.session:
            try:
                result = await db_session.execute(select(AdjacencyGraphs).where(AdjacencyGraphs.id == graph_id))
                return result.scalars().first()
            except Exception as e:
                await db_session.rollback()
                raise e
            
    async def get_adjacency_graph(self, graph_id: int) -> ListGraphsSchema:
        async for db_session in self.session:
            try:
                result = await db_session.execute(select(NodesGraphs).where(NodesGraphs.graph_id == graph_id))

                list_adj = ListGraphsSchema()
                graph_dict = {}

                for it in result.scalars().all():
                    targets = await db_session.execute(select(NodesGraphs)
                                                       .where(NodesGraphs.graph_id == graph_id)
                                                       .where(NodesGraphs.source == it.source))
                    if len(targets.scalars().all()) == 0:
                        graph_dict[it.source] = []
                    else:
                        graph_dict[it.source] = [k.target for k in targets.scalars().all()]
                list_adj.adjacency_list = graph_dict

                return list_adj
            except Exception as e:
                await db_session.rollback()
                raise e
                                    

    async def get_reverse_adjacency_graph(self, graph_id: int) -> ListGraphsSchema:
        async for db_session in self.session:
            try:
                result = await db_session.execute(select(NodesGraphs.source,
                                                         NodesGraphs).where(NodesGraphs.graph_id == graph_id))

                list_adj = ListGraphsSchema()
                reverse_graph_dict = {}

                for it in result.scalars().all():
                    targets = await db_session.execute(select(NodesGraphs)
                                                       .where(NodesGraphs.graph_id == graph_id)
                                                       .where(NodesGraphs.target == it.target))
                    if len(targets.scalars().all()) == 0:
                        reverse_graph_dict[it.target] = []
                    else:
                        reverse_graph_dict[it.target] = [k.source for k in targets.scalars().all()]
                list_adj.adjacency_list = reverse_graph_dict

                return list_adj
            except Exception as e:
                await db_session.rollback()
                raise e


    async def delete_graph(self, graph_id: int, node_name: str):
        async for db_session in self.session:
            try:
                del_graph = await db_session.execute(select(AdjacencyGraphs)
                                                     .where(AdjacencyGraphs.id == graph_id)
                                                     .where(AdjacencyGraphs.nodes == node_name))
                
                graph = del_graph.scalar_one_or_none()

                if graph is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Graph not found"
                    )

                db_session.delete(graph)
                await db_session.commit()
            except Exception as e:
                await db_session.rollback()
                raise e
        