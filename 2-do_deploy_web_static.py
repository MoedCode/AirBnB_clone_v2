#!/usr/bin/python3
# Import the necessary Fabric module
from fabric.api import run, put, env

# Define the function do_deploy that takes archive_path as a parameter


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """

    # Check if the file at the specified path exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the specified folder on the web server
        folder_name = archive_path.split('/')[-1].split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_path.split('/')[-1], folder_name))

        # Remove the uploaded archive from the web server
        run('rm /tmp/{}'.format(archive_path.split('/')[-1]))

        # Move the contents of the extracted folder to a new location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(folder_name, folder_name))

        # Remove the now-empty folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        # Remove the symbolic link to the current version
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link pointing to the deployed version
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(folder_name))

        # Print a message indicating successful deployment
        print("New version deployed!")

        return True

    except Exception as e:
        # Print an error message and return False if any step fails
        print(e)
        return False


# Set the list of web server IPs
env.hosts = ['<IP web-01>', '<IP web-02>']
