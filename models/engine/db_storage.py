#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding classes
registered_classes = {"Amenity": Amenity, "City": City,
                      "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with the MySQL database"""

    # Database engine
    __db_engine = None
    # Database session
    __db_session = None

    def __init__(self):
        """Initialize a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__db_engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                         format(HBNB_MYSQL_USER,
                                                HBNB_MYSQL_PWD,
                                                HBNB_MYSQL_HOST,
                                                HBNB_MYSQL_DB),
                                         pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__db_engine)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__db_engine)
        Session = scoped_session(sessionmaker(bind=self.__db_engine,
                                              expire_on_commit=False))
        self.__db_session = Session()

    def new(self, instance):
        """Add the object to the current database session"""
        self.__db_session.add(instance)

    def all(self, cls=None):
        """Query on the current database session"""
        result_dict = {}
        for class_name, class_type in registered_classes.items():
            if cls is None or cls is class_type or cls is class_name:
                instances = self.__db_session.query(class_type).all()
                for instance in instances:
                    key = instance.__class__.__name__ + '.' + instance.id
                    result_dict[key] = instance
        return result_dict

    def delete(self, instance=None):
        """Delete from the current database session if not None"""
        if instance is not None:
            self.__db_session.delete(instance)

    def save(self):
        """Commit all changes of the current database session"""
        self.__db_session.commit()

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__db_session.remove()
