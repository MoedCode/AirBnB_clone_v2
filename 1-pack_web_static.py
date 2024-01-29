#!/usr/bin/python3
"""Fabric script for generating a .tgz archive"""
from fabric.api import local
from datetime import datetime


def create_archive():
    """Compresses all files in the web_static folder"""
    local("mkdir -p ./versions")
    current_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    result = local(f'tar -cvzf versions/web_static_{current_time}.tgz web_static')
    if result.failed:
        return None
    else:
        print(result)
        return result
