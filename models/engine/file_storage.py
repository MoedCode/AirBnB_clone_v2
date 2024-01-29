#!/usr/bin/python3
"""Module for managing file storage in hbnb clone"""
import json


class FileStorage:
    """Manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def delete(self, obj=None):
        """delete obj from objects dictionary  if it’s inside"""
        if obj:
            for delete_ob in self.__objects:
                Idx = delete_ob.index(".")
                if obj.id == delete_ob[Idx + 1:]:
                    del (self.__objects[delete_ob])
                    self.save()
                    break

    def all(self, cls=None):
        """Returns a models dictionary  currently in storage"""
        if cls:
            result = {}
            for Key, Valueue in self.__objects.items():
                Idx = Key.index(".")
                if Key[:Idx] == cls.__name__:
                    result[Key] = Valueue
            return result
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds in storage """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, Value in temp.items():
                temp[key] = Value.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads  from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as FILE:
                temp = json.load(FILE)
                for key, Value in temp.items():
                    self.all()[key] = classes[Value['__class__']](**Value)
        except FileNotFoundError:
            pass

        def close(self):
            """ calls reload() for deserializing the JSON file to objects."""
            self.reload()
