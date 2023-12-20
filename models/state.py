#!/usr/bin/python3
""" City Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

from os import getenv


class State(BaseModel, Base):
    """ State class """

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")

    else:
        name = ""

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            cit_vals_list = []
            Cits_dict = models.storage.all('City')
            for city, value in Cits_dict.items():
                if self.id == city.state_id:
                    cit_vals_list.append(value)
            return cit_vals_list
#     """ State class """
#     name = ""
