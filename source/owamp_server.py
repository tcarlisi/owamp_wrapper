"""
owamp_server.py
    Owamp Server
@author: Thomas Carlisi
"""
import logging
import shlex
import os
import signal
from subprocess import Popen, PIPE
import warnings

class OwampServer():
    """
    Execute the owamp server process (owampd) with the previously chosen configuration
    """
    def __init__(self, dir_pid):
        self.dir_pid = dir_pid          # directory containing the pid file of the server process

    def launch_owampd(self):
        """
        Execute the owampd program.

        In fact, this is the owampd initializer that is executed, which in turn
        fork the server process (with the pid contained in the dir_pid directory)

        Execption can be raised if the initializer owampd process return a bad exit code
        """
        cmd = "../Implementation/executables/bin/owampd -c ../Implementation/config"
        process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        if exit_code != 0:
            message = "the owamp server initialization process ended with bad exit code"
            message += "owamp server (owampd) error message:" + stderr + stdout
            raise Exception(message)

    def close_owampd(self):
        """
        Close the owampd program.

        A warning is raised if the indicated pid file does not contain an executing process
        """
        with open(self.dir_pid + "/owamp-server.pid", "r") as f:
            pid = int(f.readlines()[0])
            try:
                os.kill(pid, signal.SIGTERM)
            except Exception as err:
                message = "owampd process not killed: {}\n".format(err)
                warnings.warn(message)
    
