#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""
from fabric.api import local, run, put, env
from datetime import datetime
from os import path

env.hosts = ["100.27.13.254", "54.173.155.101"]


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


def do_deploy(archive_path):
    """ distributes an archive to your web servers"""
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = path.basename(archive_path)
        target_dir_name = f"/data/web_static/releases/{file_name[:-4]}"
        run(f"sudo mkdir -p {target_dir_name}")
        run(f"sudo tar -xzf /tmp/{file_name} -C {target_dir_name}")
        run(f"sudo rm /tmp/{file_name}")
        first = f'/data/web_static/releases/{file_name[:-4]}/web_static/*'
        run(f'sudo mv {first}  /data/web_static/releases/{file_name[:-4]}/')
        run(f'sudo rm -rf {first}')
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {target_dir_name} /data/web_static/current")
        return True
    except Exception:
        return False
