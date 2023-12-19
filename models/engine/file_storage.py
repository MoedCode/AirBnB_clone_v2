#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Retrieve the dictionary's stored in objects or filter by class.
        methods parameters
        cls (optional): If specified, filter objects by the given class.
        Returns:
        dict: dictionary contains objects stored in __objects or filtered by class.
        """
        if cls is not None:
            filt_dicts = {}
            for object_key, object_instance in self.__objects.items():
                if cls == object_instance.__class__ or cls == object_instance.__class__.__name__:
                    filt_dicts[object_key] = object_instance
            return filt_dicts
        return self.__objects

    # def new(self, obj):
    #     """Adds new object to storage dictionary"""
    #     self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            new_obj_name = obj.__class__.__name__ + "." + obj.id
            self.__objects[new_obj_name] = obj

    # def save(self):
    #     """Saves storage dictionary to file"""
    #     with open(FileStorage.__file_path, 'w') as f:
    #         temp = {}
    #         temp.update(FileStorage.__objects)
    #         for key, val in temp.items():
    #             temp[key] = val.to_dict()
    #         json.dump(temp, f)
    def save(self):
        """Serializes and writes objects to the JSON file."""
        serialized_objects = {}

        # Serialize each object in __objects
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()

        # Write serialized objects to the JSON file
        with open(self.__file_path, 'w') as FILE:
            json.dump(serialized_objects, FILE)

    def delete(self, obj=None):
        """ Remove obj from the storage objects if it exist"""
        if obj is not None:
            object_key = obj.__class__.__name__ + '.' + obj.id
            if object_key in self.__objects:
                del self.__objects[object_key]

    def reload(self):
        """Loads storage dictionary from file"""
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
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
