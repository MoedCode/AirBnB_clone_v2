#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ States Class  """

    __tablename__ = 'states'
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)

        cities = relationship('City', backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ''

        @property
        def cities(self):
            """returns cities List"""
            from models import storage
            from models.city import City

            Result_list = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    Result_list.append(value)
            return Result_list
