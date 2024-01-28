#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """All files in the folder web_static"""
    local("mkdir -p ./versions")
    current_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    res = local(f'tar -cvzf versions/web_static_{current_time}.tgz web_static')
    if res.failed:
        return None
    else:
        print(res)
        return res
