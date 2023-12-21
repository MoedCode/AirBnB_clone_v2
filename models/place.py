#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Integer, Float, Table
import models
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.ext.declarative import declarative_base


if getenv("HBNB_TYPE_STORAGE") == 'db':

    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = "places"
        city_id = Column(
            String(60),
            ForeignKey(
                'cities.id',
                ondelete='CASCADE'),
            nullable=False)
        user_id = Column(
            String(60),
            ForeignKey(
                'users.id',
                ondelete='CASCADE'),
            nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        # amenity_ids = []
        reviews = relationship(
            "Review",
            cascade='all, delete',
            backref="place")
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False, overlaps='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            my_list = []
            my_dict = models.storage.all('Review')
            for key, value in my_dict.items():
                if self.id == key.place_id:
                    my_list.append(value)
            return my_list

        @property
        def amenities(self):
            """amenities method"""
            my_list = []
            my_dict = models.storage.all('Amenity')
            for key, value in my_dict.items():
                if self.id == key.amenity_ids:
                    my_list.append(value)
            return my_list

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
