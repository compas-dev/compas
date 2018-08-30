
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from paramiko import AutoAddPolicy
    from paramiko import SSHClient
except ImportError:
    pass

import os


__all__ = [
    'SSH',
]


class SSH(object):

    """ Initialse an SSH object.

    Parameters
    ----------
    username : str
        Username.
    server : str
        ssh server address.

    Returns
    -------
    None

    """

    def __init__(self, server, username):

        self.server   = server
        self.username = username
        self.client   = self.create_client()

    def create_client(self):

        """ Create SSH client with Paramiko.

        Parameters
        ----------
        None

        Returns
        -------
        obj
            ssh client object.

        """

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            client.connect(self.server, username=self.username)
            print('\n***** Connected to server: {0} with username: {1}'.format(self.server, self.username))

        except Exception:
            print('\n***** Connection failed')

        return client

    def close(self):

        """ Close the SSH object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        self.client.close()
        print('\n***** SSH connection closed')

    def receive_file(self, remote_file, local_file):

        """ Recieve a remote file from the ssh server.

        Parameters
        ----------
        remote_file : str
            Path of the remote file to recieve.
        local_file : str
            Path to save the local file as.

        Returns
        -------
        None

        """

        command = 'scp {0}@{1}:{2} {3}'.format(self.username, self.server, remote_file, local_file)
        self.local_command(command)

    def send_file(self, local_file):

        """ Send a local file to the ssh server.

        Parameters
        ----------
        local_file : str
            Path of the local file to send.

        Returns
        -------
        None

        """
        command = 'scp {0} {1}@{2}:'.format(local_file, self.username, self.server)
        self.local_command(command=command)

    def send_folder(self, local_folder):

        """ Send a local folder to the ssh server.

        Parameters
        ----------
        local_folder : str
            Path of the local folder to send.

        Returns
        -------
        None

        """

        command = 'scp -r {0} {1}@{2}:'.format(local_folder, self.username, self.server)
        self.local_command(command=command)

    def sync_folder(self, local_folder, remote_folder):

        """ Sync using rsync, a local folder to a remote folder on an ssh server.

        Parameters
        ----------
        local_folder : str
            Path of the local folder to sync from.
        remote_folder : str
            Path of the remote folder to sync to.

        Returns
        -------
        None

        """
        command = 'rsync -Pa {0} {1}@{2}:{3}'.format(local_folder, self.username, self.server, remote_folder)
        self.local_command(command=command)

    @staticmethod
    def local_command(command, folder=None):

        """ Enter a local BASH command.

        Parameters
        ----------
        command : str
            The command to execute on the local system.
        folder : str
            Local folder to execute the command from.

        Returns
        -------
        None

        """

        print('\n***** Executing local command: {0}'.format(command))

        if folder:
            os.chdir(folder)
        os.system(command)

        print('***** Done')

    def server_command(self, command):

        """ Send a BASH command to run on the ssh server.

        Parameters
        ----------
        command : str
            The command to run on the remote system.

        Returns
        -------
        None

        """

        print('\n***** Executing server command: {0}\n'.format(command))

        stdin, stdout, stderr = self.client.exec_command(command)
        for line in stdout.readlines():
            print(line)
        for line in stderr.readlines():
            print(line)

        print('***** Done')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    ssh = SSH(server='euler.ethz.ch', username='liewa')
    ssh.send_file(local_file='/home/al/downloads/test.py')
    ssh.server_command(command='ls')
    ssh.receive_file(remote_file='test.py', local_file='/home/al/downloads/test2.py')
    ssh.close()
