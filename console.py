#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import os
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    env_vars = {
        'storage_type': os.getenv('HBNB_TYPE_STORAGE', default=None),
        'running_env': os.getenv('HBNB_ENV', default=None),
        'mysql_user': os.getenv('HBNB_MYSQL_USER', default=None),
        'mysql_password': os.getenv('HBNB_MYSQL_PWD', default=None),
        'mysql_host': os.getenv('HBNB_MYSQL_HOST', default=None),
        'mysql_namedb': os.getenv('HBNB_MYSQL_DB', default=None),
    }
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)', end=" ")

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        # Split the input string into a list of arguments
        args_list = args.split(" ")
        # Check if the class name is missing
        if not args_list[0]:
            print("** class name missing **")
            return
         # Check if the class exists in the defined classes
        elif args_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[args_list[0]]()
        # Iterate through the remaining arguments (attributes) and set them
        for prop in args_list[1:]:
            # list of rest of args after class name
            tok_arg_list = prop.split("=")
            key = tok_arg_list[0]
            value = tok_arg_list[1]
            if value[0] == '"' and value[-1] == '"':
                value = str(value[1:-1])
                value = value.replace("_", " ")
            else:
                value = eval(value)
            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def display_object(self, arguments):
        """ Display details of an individual object """
        class_name, object_id = arguments.partition(" ")

        # Handle trailing arguments
        if object_id and ' ' in object_id:
            object_id = object_id.partition(' ')[0]

        # Check if class name is provided
        if not class_name:
            print("** Class name is missing **")
            return

        # Check if the provided class exists
        if class_name not in HBNBCommand.classes:
            print("** Class doesn't exist **")
            return

        # Check if instance id is provided
        if not object_id:
            print("** Instance id is missing **")
            return

        # Generate key from class and id
        key = class_name + "." + object_id

        try:
            # Display the instance details
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** No instance found **")

    def show_help(self):
        """ Display help information for the 'show' command """
        print("Shows details of an individual instance of a class")
        print("[Usage]: show <className> <objectId>")

    def destroy_object(self, arguments):
        """ Deletes a specified object """
        class_name, obj_id = arguments.partition(" ")

        # Extract only the first word if there are multiple words in obj_id
        if obj_id and ' ' in obj_id:
            obj_id = obj_id.partition(' ')[0]

        # Check if class name is missing
        if not class_name:
            print("** Class name missing **")
            return

        # Check if the specified class exists
        if class_name not in HBNBCommand.classes:
            print("** Class doesn't exist **")
            return

        # Check if instance id is missing
        if not obj_id:
            print("** Instance id missing **")
            return

        obj_key = f"{class_name}.{obj_id}"

        try:
            # Delete the object from the storage and save changes
            del storage.all()[obj_key]
            storage.save()
        except KeyError:
            print("** No instance found **")

    def display_help_all(self):
        """ Provides help information for the 'all' command """
        print("Shows all objects or all of a specific class")
        print("[Usage]: all <className>\n")

    # Command to test the method:
    # display_help_all()

    def display_all_objects(self, class_name_argument):
        """ Display all objects or all objects of a specific class. """
        object_list = []

        if class_name_argument:
            class_name_argument = class_name_argument.split(
                ' ')[0]  # Remove possible trailing args
            if class_name_argument not in HBNBCommand.classes:
                print("** Class doesn't exist **")
                return

            # Iterate through storage objects
            for key, value in storage.all(HBNBCommand.classes[class_name_argument]).items():
                if key.split('.')[0] == class_name_argument:
                    object_list.append(str(value))
        else:
            # Iterate through all storage objects
            for key, value in storage.all().items():
                object_list.append(str(value))

        print(object_list)

    def count_class_instances(self, class_name):
        """ Count current number of instances for a specific class. """
        count = 0

        # Iterate through storage objects
        for key, value in storage._FileStorage__objects.items():
            if class_name == key.split('.')[0]:
                count += 1

        print(count)

# Command to test display_all_objects method:
# do_display_all_objects <class_name_argument>
# Example: do_display_all_objects Place

    def update_object(self, args):
        """ Update attributes of a specified object """
        class_name = instance_id = attribute_name = attribute_value = kwargs = ''

        # Split class name from id/args (e.g., <cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            class_name = args[0]
        else:
            # Print an error message if class name is missing
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.classes:
            # Print an error message if the class doesn't exist
            print("** class doesn't exist **")
            return

        # Isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            instance_id = args[0]
        else:
            # Print an error message if instance id is missing
            print("** instance id missing **")
            return

        # Generate key from class and id
        key = class_name + "." + instance_id

        # Check if the key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # Determine if kwargs or args are present
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # Reformat kwargs into a list, e.g., [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # Isolate args
            args = args[2]
            if args and args[0] == '\"':
                # Check for a quoted arg
                second_quote = args.find('\"', 1)
                attribute_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # If attribute_name was not a quoted arg
            if not attribute_name and args[0] != ' ':
                attribute_name = args[0]

            # Check for a quoted value arg
            if args[2] and args[2][0] == '\"':
                attribute_value = args[2][1:args[2].find('\"', 1)]

            # If attribute_value was not a quoted arg
            if not attribute_value and args[2]:
                attribute_value = args[2].partition(' ')[0]

            args = [attribute_name, attribute_value]

        # Retrieve the dictionary of current objects
        object_dict = storage.all()[key]

        # Iterate through attribute names and values
        for i, attr_name in enumerate(args):
            # Block only runs on even iterations
            if (i % 2 == 0):
                attribute_value = args[i + 1]  # Following item is the value
                if not attribute_name:
                    # Check for attribute_name
                    print("** attribute name missing **")
                    return
                if not attribute_value:
                    # Check for attribute_value
                    print("** value missing **")
                    return

                # Type cast as necessary
                if attribute_name in HBNBCommand.types:
                    attribute_value = HBNBCommand.types[attribute_name](
                        attribute_value)

                # Update the dictionary with name, value pair
                object_dict.__dict__.update({attribute_name: attribute_value})

        object_dict.save()  # Save updates to file

    # Command to test the method
    # update_object("User 123 {'name': 'John'}")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
