#!/usr/bin/python3
"""data base storage"""

from models.base_model import BaseModel
from models.base_model import Base
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.review import Review
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

# Get values from environment variables
mysql_user = getenv("HBNB_MYSQL_USER")
mysql_pwd = getenv("HBNB_MYSQL_PWD")
mysql_host = getenv("HBNB_MYSQL_HOST")
mysql_db = getenv("HBNB_MYSQL_DB")

# Construct the database URL
db_url = f"mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}"

# Create the SQLAlchemy engine


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop.all(self.__engine)

    def all(self, cls=None):
        cls_dict = {}
        if cls is None:
            cls_list = self.__session.query(State).all()
            cls_list.extend(self.__session.query(City).all())
            cls_list.extend(self.__session.query(User).all())
            cls_list.extend(self.__session.query(Place).all())
            cls_list.extend(self.__session.query(Review).all())
            cls_list.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            cls_list = self.__session.query(cls)
        for instance in cls_list:
            key = f"{type(instance).__name__}.{instance.id}"
            cls_dict[key] = instance
        return cls_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        """   """
        if (obj):
            self.__session.delete(obj)

    def reload(self):
        """  """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
