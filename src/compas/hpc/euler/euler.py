from compas.com.ssh import ssh


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'connect_to_euler',
    'load_euler_module',
    # 'loaded_euler_modules',
    'recieve_file_from_euler',
    'send_file_to_euler',
    'send_folder_to_euler',
    'show_euler_quotas',
    'show_euler_modules',
    'show_euler_module_info',
    'sync_folder_to_euler',
    # 'unload_euler_modules',
]


server = 'euler.ethz.ch'


def connect_to_euler(username):
    """ Connect to the ETHZ Euler cluster.

    Parameters:
        username (str): Username.

    Returns:
        obj: ssh client object.
    """
    client = ssh.connect_to_server(username=username, server=server)
    return client


def load_euler_module(client, module):
    """ Load a specific Euler module.

    Parameters:
        client (obj): Connected ssh client object to Euler.
        module (str): Module to load.

    Returns:
        None
    """
    ssh.server_command(client=client, command='module load {0}; module list'.format(module))


# def loaded_euler_modules(client):
#     """ List the currently loaded Euler modules.

#     Parameters:
#         client (obj): Connected ssh client object to Euler.

#     Returns:
#         None
#     """
#     ssh.server_command(client=client, command='module list')


def recieve_file_from_euler(username, remote_file, local_file):
    """ Recieve a remote file from the ETHZ Euler cluster (home folder).

    Parameters:
        username (str): Username.
        remote_file (str); Path of remote file to recieve.
        local_file (str); Path to save local file as.

    Returns:
        None
    """
    ssh.receive_file(username=username, remote_file=remote_file, local_file=local_file, server=server)


def send_file_to_euler(username, local_file):
    """ Send a local file to the ETHZ Euler cluster (home folder).

    Parameters:
        username (str): Username.
        local_file (str); Path of local file to send.

    Returns:
        None
    """
    ssh.send_file(username=username, local_file=local_file, server=server)


def send_folder_to_euler(username, local_folder):
    """ Send a local folder to the ETHZ Euler cluster (home folder).

    Parameters:
        username (str): Username.
        local_folder (str); Path of local folder to send.

    Returns:
        None
    """
    ssh.send_folder(username=username, local_folder=local_folder, server=server)


def show_euler_quotas(username, client):
    """ Show the storage quotas for Euler user.

    Parameters:
        username (str): Username.
        client (obj): Connected ssh client object to Euler.

    Returns:
        None
    """
    ssh.server_command(client=client, command='quota -s')
    ssh.server_command(client=client, command='pan_quota /cluster/scratch/{0}'.format(username))


def show_euler_modules(client):
    """ Show the available Euler modules.

    Parameters:
        client (obj): Connected ssh client object to Euler.

    Returns:
        None
    """
    ssh.server_command(client=client, command='module avail')


def show_euler_module_info(client, module):
    """ Show the information on a specific Euler module.

    Parameters:
        client (obj): Connected ssh client object to Euler.
        module (str): Module to inspect.

    Returns:
        None
    """
    ssh.server_command(client=client, command='module show {0}'.format(module))


def sync_folder_to_euler(username, local_folder, remote_folder):
    """ Sync (rsync) a local folder to the ETHZ Euler cluster (home folder).

    Note:
        - Appropriate file/folder permissions are needed on the remote folder.

    Parameters:
        username (str): Username.
        local_folder (str); Path of local folder to sync.
        remote_folder (str); Path of remote folder to sync.

    Returns:
        None
    """
    ssh.sync_folder(username=username, local_folder=local_folder, remote_folder=remote_folder, server=server)


# def unload_euler_modules(client):
#     """ Unload all Euler modules.

#     Parameters:
#         client (obj): Connected ssh client object to Euler.

#     Returns:
#         None
#     """
#     ssh.server_command(client=client, command='module purge')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    client = connect_to_euler(username='liewa')
    sync_folder_to_euler(username='liewa', local_folder='/home/al/Dropbox/compas_core/', remote_folder='compas_core/')
    # show_euler_quotas(username='liewa', client=client)
    # show_euler_modules(client=client)
    # show_euler_module_info(client=client, module='python')
    # load_euler_module(client=client, module='python')
    client.close()
