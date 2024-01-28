#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ class for creating instance for States data """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")

    elif getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            "returns  LOAC kist of all cites "
            LOAC = list(models.storage.all(City).values())
            return [city for city in LOAC if city.state_id == self.id]
