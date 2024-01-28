#!/usr/bin/python3
"""this is class file"""
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


class db_storage:
    """this is class"""
    __engine = None
    __session = None

    def __init__(self):
        usr = os.getenv("HBNB_MYSQL_USER")
        host = os.getenv("HBNB_MYSQL_HOST")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV", "none")
        ex = f"mysql+mysqldb://{usr}:{pwd}@{host}/{db}"
        self.__engine = create_engine(ex, pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """return all or cls"""

        result = {}
        if cls is None:
            classes = [City, State, Amenity, Review, Place, User]
            for classOne in classes:
                var = self.__session.query(classOne).all()
                for obj in var:
                    objkey = f"{obj.__class__.__name__}.{obj.id}"
                    result[objkey] = obj
        else:
            var = self.__session.query(cls).all()
            for obj in var:
                objkey = f"{obj.__class__.__name__}.{obj.id}"
                result[objkey] = obj
        return result

    def new(self, obj):
        """add the object"""

        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """commit all changes"""

        self.__session.commit()

    def delete(self, obj=None):
        """delete from the db"""
        if obj is not None:
            self.__session.query(type(obj)).filter
            (type(obj).id == obj.id).delete()

    def reload(self):
        """
        create all tables in the database
        create the current database session
        """

        Base.metadata.create_all(self.__engine)
        oursession = sessionmaker(expire_on_commit=False,
                                  bind=self.__engine)
        self.__session = scoped_session(oursession)()

    def close(self):
        """ call close on private session. """
        self.__session.close()
