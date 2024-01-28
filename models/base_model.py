#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from os import getenv
import models
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Base class for HBNB models."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        self.id = str(uuid.uuid4())
        if not kwargs:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if not kwargs.get('updated_at'):
                self.updated_at = datetime.now()
            else:
                # Convert 'updated_at' string to datetime object
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if not kwargs.get('created_at'):
                self.created_at = datetime.now()
            else:
                # Convert 'created_at' string to datetime object
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls_name = type(self).__name__
        return '[{}] ({}) {}'.format(cls_name, self.id, self.__dict__)

    def save(self):
        """Updates 'updated_at' with the current time when the instance is changed."""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes the instance from storage."""
        models.FileStorage.delete(self)

    def to_dict(self):
        """Converts the instance into a dictionary format."""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': type(self).__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # Exclude SQLAlchemy instance state if present
        dictionary.pop('_sa_instance_state', None)
        return dictionary
