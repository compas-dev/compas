try:
    from paramiko import AutoAddPolicy
    from paramiko import SSHClient
except ImportError:
    pass

import os


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'connect_to_server',
    'local_command',
    'receive_file',
    'send_file',
    'send_folder',
    'sync_folder',
    'server_command'
]


def connect_to_server(username, server):
    """ Connect to an ssh server.

    Parameters:
        username (str): Username.
        server (str); ssh server address.

    Returns:
        obj: ssh client object.
    """
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        client.connect(server, username=username)
        print('\n***** Connected to server {0} with user {1} *****'.format(server, username))
    except:
        print('\n***** Connection failed *****')
    return client


def local_command(command, folder=None):
    """ Enter a local bash command.

    Parameters:
        command (str); The command to execute.
        folder (str): Local folder to execute the command in.

    Returns:
        None
    """
    print('\n***** Executing local command: {0} *****'.format(command))
    if folder:
        os.chdir(folder)
    os.system(command)


def receive_file(username, remote_file, local_file, server):
    """ Recieve a remote file from an ssh server.

    Parameters:
        username (str): Username.
        remote_file (str); Path of remote file to recieve.
        local_file (str); Path to save local file as.
        server (str); ssh server address.

    Returns:
        None
    """
    command = 'scp {0}@{1}:{2} {3}'.format(username, server, remote_file, local_file)
    local_command(command)


def send_file(username, local_file, server):
    """ Send a local file to an ssh server.

    Parameters:
        username (str): Username.
        local_file (str); Path of local file to send.
        server (str); ssh server address.

    Returns:
        None
    """
    command = 'scp {0} {1}@{2}:'.format(local_file, username, server)
    local_command(command=command)


def send_folder(username, local_folder, server):
    """ Send a local folder to an ssh server.

    Parameters:
        username (str): Username.
        local_folder (str); Path of local folder to send.
        server (str); ssh server address.

    Returns:
        None
    """
    command = 'scp -r {0} {1}@{2}:'.format(local_folder, username, server)
    local_command(command=command)


def sync_folder(username, local_folder, remote_folder, server):
    """ Sync (rsync) a local folder to a folder on an ssh server.

    Parameters:
        username (str): Username.
        local_folder (str); Path of local folder to sync.
        remote_folder (str); Path of remote folder to sync.
        server (str); ssh server address.

    Returns:
        None
    """
    command = 'rsync -Pav {0} {1}@{2}:{3}'.format(local_folder, username, server, remote_folder)
    local_command(command=command)


def server_command(client, command):
    """ Send a bash command to the ssh server.

    Parameters:
        client (obj): Connected ssh client object.
        command (str); The command to send.

    Returns:
        None
    """
    print('\n***** Executing server command: {0} *****\n'.format(command))
    stdin, stdout, stderr = client.exec_command(command)
    for line in stdout.readlines():
        print(line)
    for line in stderr.readlines():
        print(line)


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == '__main__':

    client = connect_to_server(username='liewa', server='euler.ethz.ch')
    server_command(client=client, command='ls')
    local_command(command='ls', folder='/home/al/Downloads/')
    client.close()
