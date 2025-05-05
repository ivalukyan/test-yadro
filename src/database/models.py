from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class adjancency_graphs(Base):
    __tablename__ = 'adjacency_graphs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nodes = Column()


class nodes_graphs(Base):
    id = Column(Integer, nullable=False, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("adjacency_graphs.id"), nullable=False)
    name = Column(String, nullable=False)


class edges_graphs(Base):
    id = Column(Integer, nullable=False, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("adjacency_graphs.id"), nullable=False)
    