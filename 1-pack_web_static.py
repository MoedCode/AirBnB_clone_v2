#!/usr/bin/python3
from fabric.api import local
from time import strftime


def do_pack():
    """
    Generates a compressed archive of the contents in the web_static folder.

    Returns:
        str: The path to the created archive, or None if an error occurs.
    """

    # Generate a timestamp to make the archive file unique
    filename = strftime("%Y%m%d%H%M%S")

    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Use tar to create a compressed archive of the web_static folder
        local("tar -czvf versions/web_static_{}.tgz web_static/".format(filename))

        # Return the path to the created archive
        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        # If an error occurs during the process, return None
        return None

# Example usage:
# archive_path = do_pack()
# if archive_path:
#     print(f"Archive created: {archive_path}")
# else:
#     print("Error creating archive.")
