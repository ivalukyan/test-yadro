from fastapi import HTTPException

from sqlalchemy.orm import Session, selectinload
from typing import List
from sqlalchemy import select

from src.database.models import AdjacencyGraphs, NodesGraphs, EdgesGraphs
from src.backend.schemas.schemas_graph import ListGraphsSchema, NodeSchema, EdgeSchema


class UtilsAdjacencyGraphs():
    def __init__(self, db_session: Session):
        self.session = db_session

    async def add_graph(self, nodes: List[NodeSchema], edges: List[EdgeSchema]) -> int:
        db_session = self.session
        try:
            node_models = [NodesGraphs(name=node.name) for node in nodes]
            edge_models = [EdgesGraphs(source=edge.source, target=edge.target) for edge in edges]

            new_graph = AdjacencyGraphs(nodes=node_models, edges=edge_models)
            db_session.add(new_graph)
            await db_session.commit()
            await db_session.refresh(new_graph)
            return new_graph.id
        except Exception as e:
            await db_session.rollback()
            raise e
    

    async def get_graph(self, graph_id: int) -> AdjacencyGraphs:
        try:
            result = await self.session.execute(
                select(AdjacencyGraphs)
                .options(
                    selectinload(AdjacencyGraphs.nodes),
                    selectinload(AdjacencyGraphs.edges)
                )
                .where(AdjacencyGraphs.id == graph_id)
            )
            return result.scalars().first()
        except Exception as e:
            await self.session.rollback()
            raise e
            
    async def get_adjacency_graph(self, graph_id: int) -> ListGraphsSchema:
        db_session = self.session
        try:
            result = await db_session.execute(select(NodesGraphs).where(NodesGraphs.graph_id == graph_id))

            graph_dict = {}

            for it in result.scalars().all():
                targets = await db_session.execute(select(EdgesGraphs)
                                                   .where(EdgesGraphs.graph_id == graph_id)
                                                   .where(EdgesGraphs.source == it.source))
                if len(targets.scalars().all()) == 0:
                    graph_dict[it.source] = []
                else:
                    graph_dict[it.source] = [k.target for k in targets.scalars().all()]
            return ListGraphsSchema(adjacency_list=graph_dict)
        except Exception as e:
            await db_session.rollback()
            raise e

                                    

    async def get_reverse_adjacency_graph(self, graph_id: int) -> ListGraphsSchema:
        db_session = self.session
        try:
            result = await db_session.execute(select(EdgesGraphs.source,
                                                     EdgesGraphs).where(EdgesGraphs.graph_id == graph_id))

            list_adj = ListGraphsSchema()
            reverse_graph_dict = {}

            for it in result.scalars().all():
                targets = await db_session.execute(select(EdgesGraphs)
                                                   .where(EdgesGraphs.graph_id == graph_id)
                                                   .where(EdgesGraphs.target == it.target))
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
        db_session = self.session
        try:
            del_graph = await db_session.execute(select(AdjacencyGraphs.nodes)
                                                 .where(AdjacencyGraphs.id == graph_id)
                                                 .where(NodesGraphs.name == node_name))

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
        