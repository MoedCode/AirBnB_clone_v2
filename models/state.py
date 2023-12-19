#!/usr/bin/python3
"""contains the class definition of a State and an instance """

from sqlalchemy import Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class State (Base):
    """state class proto = Base"""
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True,
                nullable=False, unique=True)
    name = Column(String(128), nullable=False)
