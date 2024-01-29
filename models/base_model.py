#!/usr/bin/python3
"""Defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from models.engine.file_storage import FileStorage
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates  model"""

        self.id = str(uuid.uuid4())
        if not kwargs:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if not kwargs.get('updated_at'):
                self.updated_at = datetime.now()
            else:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if not kwargs.get('created_at'):
                self.created_at = datetime.now()
            else:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns the instance string representation """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at attribute with current time"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """deletes the instance from the storage"""
        FileStorage.delete(self)

    def to_dict(self):
        """Convert the instance to dict format"""
        DICT = {}
        DICT.update(self.__dict__)
        DICT.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        DICT['created_at'] = self.created_at.isoformat()
        DICT['updated_at'] = self.updated_at.isoformat()
        if DICT.get('_sa_instance_state'):
            del (DICT['_sa_instance_state'])
        return DICT
