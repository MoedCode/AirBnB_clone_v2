#!/usr/bin/python3
"""Defines the Place Module for the HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from os import getenv
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False, primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=True)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
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
        reviews = None

        @property
        def reviews(self):
            """Returns reviewed places list"""
            from models import storage

            riv_ist = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    riv_ist.append(value)
            return riv_ist

        @property
        def amenities(self):
            """Returns Places amenities"""
            from models import storage
            place_sm_ist = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    place_sm_ist.append(value)
            return place_sm_ist

        @amenities.setter
        def amenities(self, value):
            """Adds Places amenities"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)
