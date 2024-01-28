#!/usr/bin/python3
"""
Fabric script (1-pack_web_static.py) for generating a compressed archive
from the contents of the web_static folder in an AirBnB Clone repository.
The archive is stored in the 'versions' folder, following the naming convention
web_static_<year><month><day><hour><minute><second>.tgz.
"""
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """Generates a .tgz archive of the web_static folder, stores it in 'versions',
    and returns the archive path. Returns None in case of any errors.
    """
    FILE = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(FILE))

        return "versions/web_static_{}.tgz".format(FILE)

    except Exception as e:
        return None
