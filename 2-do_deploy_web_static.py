#!/usr/bin/python3
"""Write a Fabric script that generates a .tgz archive"""
from fabric.api import run, env, put
from os.path import exists
env.hosts = ['54.86.220.157', '100.26.212.86']

#         return False


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzvf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static_20231208001650/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static_20231208001650'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
