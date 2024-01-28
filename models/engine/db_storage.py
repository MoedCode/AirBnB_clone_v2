#!/usr/bin/python3
"""Defines a class for managing DB Storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from models.base_model import Base
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"City": City, "State": State, "Place": Place, "Review": Review,
           "Amenity": User, "User": Amenity
           }


class db_storage:
    """Database storage class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize database connection"""
        user = os.getenv("HBNB_MYSQL_USER")
        host = os.getenv("HBNB_MYSQL_HOST")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV", "none")
        connection_string = f"mysql+mysqldb://{user}:{pwd}@{host}/{db}"
        self.__engine = create_engine(connection_string, pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def get_all(self, cls=None):
        """Return all objects or objects of a specific class"""
        result = {}
        if cls is None:
            classes = [City, State, Amenity, Review, Place, User]
            for class_instance in classes:
                objects = self.__session.query(class_instance).all()
                for obj in objects:
                    obj_key = f"{obj.__class__.__name__}.{obj.id}"
                    result[obj_key] = obj
        else:
            objects = self.__session.query(cls).all()
            for obj in objects:
                obj_key = f"{obj.__class__.__name__}.{obj.id}"
                result[obj_key] = obj
        return result

    def add_object(self, obj):
        """Add an object to the database session"""
        if obj is not None:
            self.__session.add(obj)

    def commit_changes(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete_object(self, obj=None):
        """Delete an object from the database"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload_database(self):
        """Create tables and the current database session"""
        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(
            expire_on_commit=False, bind=self.__engine)
        self.__session = scoped_session(session_maker)()

    def close_session(self):
        """Close the private database session"""
        self.__session.close()
