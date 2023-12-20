#!/usr/bin/python3
"""This module defines a class to manage DB Storage for hbnb clone"""
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

classes = {"City": City, "State": State}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'. format(
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_DB),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """loading from database to inmemory"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def new(self, obj):
        """add new instance to Dictionary """
        self.__session.add(obj)

    def all(self, cls=None):
        strd_dict = {}
        if cls is None:
            for inst in classes:
                TABLE = self.__session.query(classes[inst]).all()
        else:
            TABLE = self.__session.query(cls).all()
        for inst in TABLE:
            key = f"{inst.__class__.__name__}.{inst.id}"
            strd_dict[key] = inst
        return strd_dict

    def save(self):
        """save and current database  changes to session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from database session"""
        if obj is None:
            return
        self.__session.delete(obj)
