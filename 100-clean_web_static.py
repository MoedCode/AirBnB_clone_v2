#!/usr/bin/python3
def do_clean(number=0):
    """Deletes out-of-date archives."""
    if number < 0:
        return
    number = 1 if number == 0 else number

    with cd('/data/web_static/releases'):
        # List all archives in versions folder
        archives = run("ls -lt versions").split()
        archives = [
            archive for archive in archives if archive.startswith('web_static_')]

        # Sort archives by modification time in reverse order
        archives.sort(key=lambda x: datetime.strptime(
            x.split('.')[0], 'web_static_%Y%m%d%H%M%S'), reverse=True)

        # Keep only the required number of archives
        archives_to_keep = archives[:number]

        # Delete unnecessary archives
        for archive in archives:
            if archive not in archives_to_keep:
                run("rm -f versions/{}".format(archive))
