#!/usr/bin/python3
"""This module defines a class to manage file storage for the HBNB clone"""
import json


class FileStorage:
    """This class manages storage of HBNB models in JSON format"""
    FILE_PATH = 'file.json'
    OBJECTS = {}

    def delete_instance(self, obj=None):
        """Deletes 'obj' from 'OBJECTS' if it’s inside"""
        if obj:
            for delete_key in list(self.OBJECTS.keys()):
                index_of_dot = delete_key.index(".")
                if obj.id == delete_key[index_of_dot + 1:]:
                    del (self.OBJECTS[delete_key])
                    self.save()
                    break

    def get_all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            result = {}
            for obj_key, obj_value in self.OBJECTS.items():
                index_of_dot = obj_key.index(".")
                if obj_key[:index_of_dot] == cls.__name__:
                    result[obj_key] = obj_value
            return result
        else:
            return FileStorage.OBJECTS

    def add_instance(self, obj):
        """Adds a new object to the storage dictionary"""
        self.get_all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save_to_file(self):
        """Saves the storage dictionary to the file"""
        with open(FileStorage.FILE_PATH, 'w') as f:
            temp = {}
            temp.update(FileStorage.OBJECTS)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def load_from_file(self):
        """Loads the storage dictionary from the file"""
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
            with open(FileStorage.FILE_PATH, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.get_all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close_connection(self):
        """Calls load_from_file() for deserializing the JSON file to objects"""
        self.load_from_file()
