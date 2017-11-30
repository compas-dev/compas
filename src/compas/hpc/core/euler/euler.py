from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.com.ssh import ssh


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'connect_to_euler',
    'load_euler_module',
    # 'loaded_euler_modules',
    'recieve_file_from_euler',
    'send_file_to_euler',
    'send_folder_to_euler',
    'show_euler_jobs',
    'show_euler_quotas',
    'show_euler_modules',
    'show_euler_module_info',
    'show_euler_resources',
    'submit_job',
    'kill_job',
    'sync_folder_to_euler',
    # 'unload_euler_modules',
]


server = 'euler.ethz.ch'


def connect_to_euler(username):
    """ Connect to the ETHZ Euler cluster.

    Parameters
    ----------
        username (str): Username.

    Returns
    -------
        obj: ssh client object.
    """
    client = ssh.connect_to_server(username=username, server=server)
    return client


def kill_job(client, job):
    """ Kill a specific submitted job on Euler.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.
        job (int): Euler job number.

    Returns
    -------
        None
    """
    ssh.server_command(client=client, command='bkill {0}'.format(job))


def load_euler_module(client, module):
    """ Load a specific Euler module.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.
        module (str): Module to load.

    Returns
    -------
        None
    """
    ssh.server_command(client=client, command='module load {0}: module list'.format(module))


# def loaded_euler_modules(client):
#     """ List the currently loaded Euler modules.

#     Parameters
#     ----------
#         client (obj): Connected ssh client object to Euler.

#     Returns
#     -------
#         None
#     """
#     ssh.server_command(client=client, command='module list')


def recieve_file_from_euler(username, remote_file, local_file):
    """ Recieve a remote file from the ETHZ Euler cluster (home folder).

    Parameters
    ----------
        username (str): Username.
        remote_file (str): Path of remote file to recieve.
        local_file (str): Path to save local file as.

    Returns
    -------
        None
    """
    ssh.receive_file(username=username, remote_file=remote_file, local_file=local_file, server=server)


def send_file_to_euler(username, local_file):
    """ Send a local file to the ETHZ Euler cluster (home folder).

    Parameters
    ----------
        username (str): Username.
        local_file (str): Path of local file to send.

    Returns
    -------
        None
    """
    ssh.send_file(username=username, local_file=local_file, server=server)


def send_folder_to_euler(username, local_folder):
    """ Send a local folder to the ETHZ Euler cluster (home folder).

    Parameters
    ----------
        username (str): Username.
        local_folder (str): Path of local folder to send.

    Returns
    -------
        None
    """
    ssh.send_folder(username=username, local_folder=local_folder, server=server)


def show_euler_quotas(username, client):
    """ Show the storage quotas for Euler user.

    Parameters
    ----------
        username (str): Username.
        client (obj): Connected ssh client object to Euler.

    Returns
    -------
        None
    """
    ssh.server_command(client=client, command='quota -s')
    ssh.server_command(client=client, command='pan_quota /cluster/scratch/{0}'.format(username))


def show_euler_modules(client):
    """ Show the available Euler modules.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.

    Returns
    -------
        None
    """
    ssh.server_command(client=client, command='module avail')


def show_euler_module_info(client, module):
    """ Show the information on a specific Euler module.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.
        module (str): Module to inspect.

    Returns
    -------
        None
    """
    ssh.server_command(client=client, command='module show {0}'.format(module))


def show_euler_resources(client):
    """ Show the available Euler resources for user.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.

    Returns
    -------
        None
    """
    ssh.server_command(client=client, command='busers')


def show_euler_jobs(client, type='user'):
    """ Show the jobs in queue on Euler.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.
        type (str): 'all' cluster jobs or those submitted by 'user'.

    Returns
    -------
        None
    """
    if type == 'all':
        ssh.server_command(client=client, command='bqueues')
    elif type == 'user':
        ssh.server_command(client=client, command='bbjobs')


def submit_job(client, command, time='60', output='output.txt', cpus=1):
    """ Submit a job to Euler.

    Notes
    -----
        - If the output file already exists, it will be overwritten.
        - STRICTLY do not request more than 24 CPUs, make sure the job can use all those requested.

    Parameters
    ----------
        client (obj): Connected ssh client object to Euler.
        command (str): Command to execute.
        time (str): Requested amount of CPU time '1:30' (hrs:mins) or '60' (mins).
        output (str): Name of output summary file.
        cpus (int): Number of CPUs to request.

    Returns
    -------
        None
    """
    n = min([24, int(cpus)])
    cmd = 'export OMP_NUM_THREADS={0}: bsub -n {0} -W {1} -oo {2} {3}: bbjobs'.format(n, int(time), output, command)
    ssh.server_command(client=client, command=cmd)


def sync_folder_to_euler(username, local_folder, remote_folder):
    """ Sync (rsync) a local folder to the ETHZ Euler cluster (home folder).

    Notes
    -----
        - Appropriate file/folder permissions are needed on the remote folder.

    Parameters
    ----------
        username (str): Username.
        local_folder (str): Path of local folder to sync.
        remote_folder (str): Path of remote folder to sync.

    Returns
    -------
        None
    """
    ssh.sync_folder(username=username, local_folder=local_folder, remote_folder=remote_folder, server=server)


# def unload_euler_modules(client):
#     """ Unload all Euler modules.

#     Parameters
#     ----------
#         client (obj): Connected ssh client object to Euler.

#     Returns
#     -------
#         None
#     """
#     ssh.server_command(client=client, command='module purge')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    client = connect_to_euler(username='liewa')
    # sync_folder_to_euler(username='liewa', local_folder='/home/al/Dropbox/compas_core/', remote_folder='compas_core/')
    # show_euler_quotas(username='liewa', client=client)
    # show_euler_modules(client=client)
    # show_euler_module_info(client=client, module='python')
    # load_euler_module(client=client, module='python')
    show_euler_resources(client=client)
    show_euler_jobs(client=client, type='all')
    submit_job(client=client, command='./test', time='5', output='output.txt', cpus=2)
    client.close()
