#!/usr/bin/python3
"""
Contains the FileStorage class
"""

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
           'State': State, 'City': City, 'Amenity': Amenity,
           'Review': Review}

class FileStorage:
    """Crating file based database throw Serializes/deSerializes json obj"""

    __file_path = "file.json"
    __objects = {}

    def reload(self):
        """JSON file deserialization the  store it  __objects """
        try:
            with open(self.__file_path, 'r') as FILE:
                json_obj = json.load(FILE)
            for key, Value in json_obj:
                self.all()[key] = classes[ Value['__class__']](**Value)
        except FileNotFoundError:
            pass

    def new(self, obj):
        """Adds a new instance to __objects with key <instance class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def all(self, cls=None):
        """Returns the dictionary __objects or filtered by class"""
        if cls is not None:
            filtered_objects = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    filtered_objects[key] = value
            return filtered_objects
        return self.__objects

    def save(self):
        """ __objects serialization to store in JSON file  __file_path"""
        serialized_objects = {}
        for key in self.__objects:
            serialized_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(serialized_objects, f)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
