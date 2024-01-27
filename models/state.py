#!/usr/bin/python3
"""
State Module for the HBNB project.
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """
    State class for storing state information.

    Attributes:
        __tablename__ (str): The table name for database storage.
        name (str): The name of the state.
        cities (relationship): Relationship with the City class.
    """

    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")

    elif getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Getter method for cities property.

            Returns:
                list: List of City instances related to the current State.
            """
            cities_list = list(models.storage.all(City).values())
            return [city for city in cities_list if city.state_id == self.id]
