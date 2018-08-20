
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.com.ssh.ssh import SSH


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'EulerSSH',
]


class EulerSSH(SSH):

    """ Initialse an EulerSSH object.

    Parameters
    ----------
    username : str
        Username.
    server : str
        Euler ssh server address.

    Returns
    -------
    None

    """

    def __init__(self, username, server='euler.ethz.ch'):
        SSH.__init__(self, server=server, username=username)

        pass

    def show_quotas(self):

        """ Show the storage quotas for the Euler user.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        self.server_command(command='quota -s')
        self.server_command(command='pan_quota /cluster/scratch/{0}'.format(self.username))

    def available_modules(self, module=None):

        """ Show the available Euler modules.

        Parameters
        ----------
        module : str
            Name of a specific module.

        Returns
        -------
        None

        """

        if module:
            self.server_command(command='module avail {0}'.format(module))
        else:
            self.server_command(command='module avail')

    def show_module(self, module):

        """ Show information on a specific Euler module.

        Parameters
        ----------
        module : str
            Module to inspect.

        Returns
        -------
        None

        """

        self.server_command(command='module show {0}'.format(module))

    def load_module(self, module):

        """ Load an Euler module.

        Parameters
        ----------
        module : str
            Module to load.

        Returns
        -------
        None

        """

        self.server_command(command='module load {0} '.format(module))

    def loaded_modules(self):

        """ List the currently loaded Euler modules.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        self.server_command(command='module list')

    def unload_modules(self):

        """ Unload all Euler modules.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        self.server_command(command='module purge')

    def submit_job(self, command, time='60', output='output.txt', mem=256, cpus=1):

        """ Submit a job to Euler.

        Parameters
        ----------
        command : str
            Command to execute.
        time : str
            Requested amount of CPU time '1:30' (hrs:mins) or '60' (mins).
        output : str
            Name of the output summary file.
        mem : int
            Requested RAM in MB per CPU.
        cpus : int
            Number of CPUs to request.

        Returns
        -------
        None

        Notes
        -----
        - If the output file already exists in /cluster/home/user/ it will be overwritten.
        - STRICTLY do not request more than 24 CPUs, make sure the job can use all those requested.

        """

        n = min([24, int(cpus)])
        cmd = 'bsub -R "rusage[mem={0}]" -n {1} -W {2} -oo {3} {4}'.format(mem, n, int(time), output, command)
        self.server_command(command=cmd)

    def show_jobs(self, type='user', job=None):

        """ Show the jobs in queue on Euler.

        Parameters
        ----------
        type : str
            'all' or 'user' Euler jobs.
        job : int
            Job number

        Returns
        -------
        None

        """

        if type == 'all':
            self.server_command(command='bqueues')

        elif type == 'user':
            if job:
                self.server_command(command='bbjobs {0}'.format(job))
            else:
                self.server_command(command='bbjobs')

    def show_resources(self):

        """ Show the available Euler resources for the user.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        self.server_command(command='busers')

    def peek_job(self, job):

        """ View the curent terminal output of a running job.

        Parameters
        ----------
        job : int
            Job number

        Returns
        -------
        None

        """

        self.server_command(command='bpeek {0}'.format(job))

    def cpu_load_job(self, job):

        """ View the CPU load of a completed job.

        Parameters
        ----------
        job : int
            Job number

        Returns
        -------
        None

        """

        self.server_command(command='lsf_load {0}'.format(job))

    def kill_job(self, job):

        """ Kill a submitted job on Euler.

        Parameters
        ----------
        job : int, str
            Job number, or 'all' jobs.

        Returns
        -------
        None

        """

        if job == 'all':
            job = 0
        self.server_command(command='bkill {0}'.format(job))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    euler_ssh = EulerSSH(username='liewa')

    euler_ssh.sync_folder(local_folder='/home/al/compas/', remote_folder='compas/')

    euler_ssh.load_module(module='python/3.6.0')
    euler_ssh.show_module(module='python/3.6.0')
    euler_ssh.loaded_modules()
    euler_ssh.available_modules()

    euler_ssh.show_resources()
    euler_ssh.show_quotas()

    euler_ssh.server_command(command='export OMP_NUM_THREADS=24')
    euler_ssh.submit_job(command='python /cluster/home/liewa/script.py',
                         time='20', output='output.txt', mem=256, cpus=4)
    euler_ssh.show_jobs(type='user', job=58152512)

    euler_ssh.receive_file(remote_file='/cluster/home/liewa/output.txt',
                           local_file='/home/al/output.txt')

    euler_ssh.close()
