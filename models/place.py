#!/usr/bin/python
""" Defines the Place class """
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base

# Check the storage type to determine whether to use a database table for place_amenity relationship
if getenv("HBNB_TYPE_STORAGE") == 'db':

    # Define the association table for the many-to-many relationship between Place and Amenity
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Place(BaseModel, Base):
    """Representation of Place"""

    # Check the storage type to determine whether to use a database table for Place
    if getenv("HBNB_TYPE_STORAGE") == 'db':

        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        # Define the relationship with Review and Amenity
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)
    else:
        # Define attributes for non-database storage
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Check if the storage type is a database, then define additional properties
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        @property
        def reviews(self):
            """ Returns the list of Review instances related to the place """
            from models.review import Review
            REV_LIST = []
            STOR_REV = models.storage.all(Review)
            for REV in STOR_REV.values():
                if REV.place_id == self.id:
                    REV_LIST.append(REV)
            return REV_LIST

        @property
        def amenities(self):
            """Returns the list of Amenity instances related to the place"""
            from models.amenity import Amenity
            AMIT_LIST = []
            STOR_AMIT = models.storage.all(Amenity)
            for AMIT in STOR_AMIT.values():
                if AMIT.place_id == self.id:
                    AMIT_LIST.append(AMIT)
            return AMIT_LIST
