from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AdjacencyGraphs(Base):
    __tablename__ = 'adjacency_graphs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nodes = relationship("NodesGraphs", back_populates="graph", cascade="all, delete-orphan")
    edges = relationship("EdgesGraphs", back_populates="graph", cascade="all, delete-orphan")

class NodesGraphs(Base):
    __tablename__ = "nodes_graphs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("adjacency_graphs.id"), nullable=False)
    name = Column(String, nullable=False)
    graph = relationship("AdjacencyGraphs", back_populates="nodes")

class EdgesGraphs(Base):
    __tablename__ = "edges_graphs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("adjacency_graphs.id"), nullable=False)
    source = Column(String, nullable=False)
    target = Column(String, nullable=False)
    graph = relationship("AdjacencyGraphs", back_populates="edges")
