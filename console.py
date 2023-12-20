#!/usr/bin/python3
""" HBNB Console Module """

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # Used for splitting the line along spaces, except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """Interactive command-line console for HBNB data management"""

    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exit the console"""
        return True

    def emptyline(self):
        """Ignore empty lines"""
        return False

    def do_quit(self, arg):
        """Quit the console"""
        return True

    def _key_value_parser(self, args):
        """Parse a list of strings into a dictionary"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Create a new instance of a class"""
        args = arg.split()
        if not args:
            print("** Class name missing **")
            return False
        if args[0] in classes:
            new_instance_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_instance_dict)
        else:
            print("** Class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Show details of an instance based on class and ID"""
        args = shlex.split(arg)
        if not args:
            print("** Class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** No instance found **")
            else:
                print("** Instance ID missing **")
        else:
            print("** Class doesn't exist **")

    def do_destroy(self, arg):
        """Destroy an instance based on class and ID"""
        args = shlex.split(arg)
        if not args:
            print("** Class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** No instance found **")
            else:
                print("** Instance ID missing **")
        else:
            print("** Class doesn't exist **")

    def do_all(self, arg):
        """Show string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if not args:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** Class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on class, ID, attribute, and value"""
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if not args:
            print("** Class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except ValueError:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except ValueError:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** Value missing **")
                    else:
                        print("** Attribute name missing **")
                else:
                    print("** No instance found **")
            else:
                print("** Instance ID missing **")
        else:
            print("** Class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
