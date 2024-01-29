#!/usr/bin/python3
""" Module for the Amenity class in the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Amenity class representing various amenities """
    __tablename__ = "amenities"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
    else:
        name = ''
