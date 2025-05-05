from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, BigInteger, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'adjacency_graphs'

    id = Column(Integer, primary_key=True)
    