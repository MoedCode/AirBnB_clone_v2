#!/usr/bin/python3
"""
This module defines the FileStorage class for managing file storage in JSON
format for the hbnb clone project.
"""

import json


class FileStorage:
    """
    FileStorage class manages storage of hbnb models in JSON format.

    Attributes:
        __file_path (str): The file path for JSON storage.
        __objects (dict): A dictionary to store serialized objects.
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all stored objects or filtered by class.

        Args:
            cls (str or class, optional): Class name or class object for
                filtering. Defaults to None.

        Returns:
            dict: A dictionary containing all objects or filtered objects.
        """
        cls_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.

        Args:
            obj: The object to be added.
        """
        class_name = type(obj).__name__
        obj_id = obj.id
        key = f"{class_name}.{obj_id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes the storage dictionary to the JSON file (__file_path).
        """
        objs = self.__objects
        objs_dict = {key: objs[key].to_dict() for key in objs.keys()}
        with open(self.__file_path, mode='w') as file_json:
            json.dump(objs_dict, file_json)

    def reload(self):
        """
        Loads the storage dictionary from the file and instantiates objects.
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
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes the specified object from the storage dictionary.

        Args:
            obj: The object to be deleted.
        """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """
        Calls the reload method to load storage from file.
        """
        self.reload()
