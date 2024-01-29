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
        """Preprocesses command line for advanced syntax.

        Usage: <class name>.<command>([<id> [<*args_list> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        command_name = class_name = instance_id = args_list = ''  # Initialize line elements

        # Check for general formatting - i.e., '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Parse line left to right
            parsed_line = line[:]  # Parsed line

            # Isolate <class name>
            class_name = parsed_line[:parsed_line.find('.')]

            # Isolate and validate <command>
            command_name = parsed_line[parsed_line.find('.') + 1:parsed_line.find('(')]
            if command_name not in HBNBCommand.dot_cmds:
                raise Exception

            # If parentheses contain arguments, parse them
            parsed_line = parsed_line[parsed_line.find('(') + 1:parsed_line.find(')')]
            if parsed_line:
                # Partition args_list: (<id>, [<delim>], [<*args_list>])
                parsed_line = parsed_line.partition(', ')  # Parsed line converted to tuple

                # Isolate instance_id, stripping quotes
                instance_id = parsed_line[0].replace('\"', '')
                # Possible bug here: empty quotes register as empty instance_id when replaced

                # If arguments exist beyond instance_id
                parsed_line = parsed_line[2].strip()  # Parsed line is now str
                if parsed_line:
                    # Check for *args_list or **kwargs
                    if parsed_line[0] == '{' and parsed_line[-1] == '}'\
                            and type(eval(parsed_line)) is dict:
                        args_list = parsed_line
                    else:
                        args_list = parsed_line.replace(',', '')
                        # args_list = args_list.replace('\"', '')
            line = ' '.join([command_name, class_name, instance_id, args_list])

        except Exception:
            pass
        finally:
            return line

    # Example command to te

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

    def do_create(self, args_list):
        """Create an instance of any class"""
        splt_args = args_list.split(" ")
        if not splt_args[0]:
            print("** class name missing **")
            return
        elif splt_args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[splt_args[0]]()
        for prop in splt_args[1:]:
            new = prop.split("=")
            key = new[0]
            value = new[1]
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

    def do_show(self, args_list):
        """ Display details of an individual object """
        new = args_list.partition(" ")
        Class_name = new[0]
        Class_ID = new[2]

        # guard against trailing args_list
        if Class_ID and ' ' in Class_ID:
            Class_ID = Class_ID.partition(' ')[0]

        if not Class_name:
            print("** class name missing **")
            return

        if Class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not Class_ID:
            print("** instance id missing **")
            return

        key = Class_name + "." + Class_ID
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def destroy_object(self, args_list):
        """Remove all instance"""
        class_name, instance_id = args_list.partition(" ")[0], args_list.partition(" ")[2].partition(" ")[0]
        if not class_name:
            print("** Class name missing. **")
            return
        if class_name not in HBNBCommand.classes:
            print("** Class doesn't exist. **")
            return
        if not instance_id:
            print("** Instance ID missing. **")
            return

        key = f"{class_name}.{instance_id}"

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** No instance found. **")

    def help_destroy_object(self):
        """Provides help information for the destroy_object command."""
        print("Deletes an individual instance of a class.")
        print("[Usage]: destroy_object <className> <objectId>")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args_list):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args_list:
            args_list = args_list.split(' ')[0]  # remove possible trailing args_list
            if args_list not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for Key, Value in storage.all(HBNBCommand.classes[args_list]).items():
                if Key.split('.')[0] == args_list:
                    print_list.append(str(Value))
        else:
            for Key, Value in storage.all().items():
                print_list.append(str(Value))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args_list):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args_list == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args_list):
        """ Updates a certain object with new info """
        Class_name = Class_ID = att_name = att_val = kwargs = ''

        # isolate cls from id/args_list, ex: (<cls>, delim, <id/args_list>)
        args_list = args_list.partition(" ")
        if args_list[0]:
            Class_name = args_list[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if Class_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args_list
        args_list = args_list[2].partition(" ")
        if args_list[0]:
            Class_ID = args_list[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = Class_name + "." + Class_ID

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args_list
        if '{' in args_list[2] and '}' in args_list[2] and type(eval(args_list[2])) is dict:
            kwargs = eval(args_list[2])
            args_list = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args_list.append(k)
                args_list.append(v)
        else:  # isolate args_list
            args_list = args_list[2]
            if args_list and args_list[0] == '\"':  # check for quoted arg
                second_quote = args_list.find('\"', 1)
                att_name = args_list[1:second_quote]
                args_list = args_list[second_quote + 1:]

            args_list = args_list.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args_list[0] != ' ':
                att_name = args_list[0]
            # check for quoted val arg
            if args_list[2] and args_list[2][0] == '\"':
                att_val = args_list[2][1:args_list[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args_list[2]:
                att_val = args_list[2].partition(' ')[0]

            args_list = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args_list):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args_list[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
