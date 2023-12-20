#!/usr/bin/python3
""" holds class User"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Representation of a user """
    # Database columns if using SQLAlchemy
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

# class User(BaseModel):
#     """This class defines a user by various attributes"""
#     email = ''
#     password = ''
#     first_name = ''
#     last_name = ''
