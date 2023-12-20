#!/usr/bin/python3
""" holds class User"""
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Representation of a user """
    # Database columns if using SQLAlchemy
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'users'
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        places = relationship("Place", cascade='all, delete', backref="user")
        reviews = relationship("Review", cascade='all, delete', backref="user")

    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# class User(BaseModel):
#     """This class defines a user by various attributes"""
#     email = ''
#     password = ''
#     first_name = ''
#     last_name = ''
