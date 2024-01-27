#!/usr/bin/python3
"""Write a Fabric script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """Trying to do that"""
    try:
        data = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(data)
        local(f"tar -cvzf {file_name} web_static")
        return file_name
    except FileExistsError:
        return None
