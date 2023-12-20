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


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")

    elif getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            Cit_inst_list = []
            for city in list(models.storage.all(City).values()):
                if City.state_id == self.id:
                    Cit_inst_list.append(City)
            return Cit_inst_list
# class State(BaseModel):
#     """ State class """
#     name = ""
