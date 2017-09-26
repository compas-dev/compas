from paramiko import AutoAddPolicy
from paramiko import SSHClient

from subprocess import Popen
from subprocess import PIPE


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'connect_to_server',
    'local_command',
    'receive_file',
    'send_file',
    'server_command'
]


def connect_to_server(username, server='euler.ethz.ch'):
    """ Connect to an ssh server.

    Parameters:
        username (str): Username.
        server (str); ssh server address.

    Returns:
        obj: ssh object.
    """
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(server, username=username)
        print('Connected to {0}\n'.format(server))
    except:
        print('Connection failed\n')
    return ssh


def local_command(command):
    """ Enter a command in a local terminal.

    Parameters:
        command (str); The command to execute.

    Returns:
        None
    """
    print('Executing command: {0}\n'.format(command))
    p = Popen([command], stdout=PIPE, stderr=PIPE, shell=True)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.strip()
        print(line)
    stdout, stderr = p.communicate()
    print(stdout)
    print(stderr)


def receive_file(username, remote_file, local_file, server='euler.ethz.ch'):
    """ Recieve a file from an ssh server.

    Parameters:
        username (str): Username.
        remote_file (str); Path for remote file.
        local_file (str); Path to save local file.
        server (str); ssh server address.

    Returns:
        None
    """
    command = 'scp {0}@{1}:{2} {3}'.format(username, server, remote_file, local_file)
    local_command(command)


def send_file(username, local_file, server='euler.ethz.ch'):
    """ Send a file to an ssh server.

    Parameters:
        username (str): Username.
        local_file (str); Path of local file to send.
        server (str); ssh server address.

    Returns:
        None
    """
    command = 'scp {0} {1}@{2}:'.format(local_file, username, server)
    local_command(username, command)


def server_command(ssh, command):
    """ Send a terminal command to the ssh server.

    Parameters:
        ssh (obj): Connected ssh object.
        command (str); The command to send.

    Returns:
        None
    """
    print('Executing command: {0}\n'.format(command))
    stdin, stdout, stderr = ssh.exec_command(command)
    for line in stdout.readlines():
        print(line.strip())


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    ssh = connect_to_server(username='liewa')
    server_command(ssh, 'module load openblas/0.2.13_par')
    server_command(ssh, 'module load python/2.7')
    server_command(ssh, 'OMP_NUM_THREADS=24')
    server_command(ssh, 'bjobs')
    ssh.close()
