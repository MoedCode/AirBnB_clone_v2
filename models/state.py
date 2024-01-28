#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)

        cities = relationship('City', backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ''

        @property
        def cities(self):
            """returns the list of City"""
            from models import storage
            from models.city import City

            result = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    result.append(value)
            return result
