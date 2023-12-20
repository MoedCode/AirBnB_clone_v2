#!/usr/bin/python3
""" City Module for HBNB project """
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models
from models.base_model import BaseModel, Base
from models.base_model import BaseModel
from models.city import City


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")

# class User(BaseModel):
#     """This class defines a user by various attributes"""
#     email = ''
#     password = ''
#     first_name = ''
#     last_name = ''
