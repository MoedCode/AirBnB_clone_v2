#!/usr/bin/python3
"""Defines a class for managing DB Storage for hbnb clone"""
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
import sqlalchemy as db

classes = {"City": City, "State": State, "Place": Place, "Review": Review,
           "Amenity": User, "User": Amenity
           }


class DBStorage:
    """Class for managing DB Storage for hbnb clone"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage instance"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Reloads the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def new(self, obj):
        """Adds a new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj is None:
            return
        self.__session.delete(obj)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        my_dict = {}
        if cls is None:
            for obj in classes:
                table = self.__session.query(classes[obj]).all()
                for obj in table:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    my_dict[key] = obj
            return my_dict
        else:
            table = self.__session.query(cls).all()
        for obj in table:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            my_dict[key] = obj
        return my_dict

    def close(self):
        """Closes the session"""
        self.__session.remove()
