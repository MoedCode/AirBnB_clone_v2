#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")

    elif getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            cities_list = list(models.storage.all(City).values())
            return [city for city in cities_list if city.state_id == self.id]
