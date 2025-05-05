from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AdjancencyGraphs(Base):
    __tablename__ = 'adjacency_graphs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nodes = relationship("NodesGraphs", back_populates="graph", cascade="all, delete-orphan")
    edges = relationship("EdgesGraphs", back_populates="graph", cascade="all, delete-orphan")


class NodesGraphs(Base):
    id = Column(Integer, nullable=False, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("adjacency_graphs.id"), nullable=False)
    name = Column(String, nullable=False)


class EdgesGraphs(Base):
    id = Column(Integer, nullable=False, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("adjacency_graphs.id"), nullable=False)
    