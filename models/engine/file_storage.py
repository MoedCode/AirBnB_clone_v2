#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding classes
registered_classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                      "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Serializes instances to a JSON file and deserializes back to instances"""

    # String - Path to the JSON file
    __file_path = "file.json"
    # Dictionary - Empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects or filtered by class"""
        if cls is not None:
            filtered_objects = {}
            for key, obj in self.__objects.items():
                if cls == obj.__class__ or cls == obj.__class__.__name__:
                    filtered_objects[key] = obj
            return filtered_objects
        return self.__objects

    def new(self, instance):
        """Adds a new instance to __objects with key <instance class name>.id"""
        if instance is not None:
            key = instance.__class__.__name__ + "." + instance.id
            self.__objects[key] = instance

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        serialized_objects = {key: obj.to_dict()
                              for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as file:
                serialized_objects = json.load(file)
            for key, data in serialized_objects.items():
                self.__objects[key] = registered_classes[data["__class__"]](
                    **data)
        except FileNotFoundError:
            pass

    def delete(self, instance=None):
        """Deletes instance from __objects if it exists"""
        if instance is not None:
            key = f"{instance.__class__.__name__}.{instance.id}"
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects"""
        self.reload()
