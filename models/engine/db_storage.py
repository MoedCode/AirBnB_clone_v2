#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from models.base_model import Base
import sys
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Add the path to the directory containing the models package to sys.path
sys.path.append('/mnt/c/Users/Active/Desktop/Coding/AirBnB_clone_v2/')


class DBStorage:
    """This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a new DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries all objects of a certain class from the database"""
        from models import classes

        objects = {}
        if cls:
            print("if")
            query_result = self.__session.query(classes[cls]).all()
        else:

            query_result = []
            for class_name in classes.values():
                query_result.extend(self.__session.query(class_name).all())

        for obj in query_result:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            objects[key] = obj

        return objects

    def new(self, obj):
        """Adds a new object to the database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes a new session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Closes the current session"""
        self.__session.remove()
