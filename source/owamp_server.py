"""
owamp_server.py
    Owamp Server
@author: Thomas Carlisi
"""
import logging
import shlex
import os
import signal
import warnings
from subprocess import Popen, PIPE

class OwampServer():
    """
    Execute the owamp server process (owampd) with the previously chosen configuration
    """
    def __init__(self, config_store):
        self.dir_pid = config_store.dir_pid                         # directory containing the pid file of the server process
        self.owamp_executable = config_store.owamp_executable       # owampd executable
        self.server_config_dir = config_store.server_config_dir     # server config directory

    def launch_owampd(self):
        """
        Execute the owampd program.

        In fact, this is the owampd initializer that is executed, which in turn
        fork the server process (with the pid contained in the dir_pid directory)

        Execption can be raised if the initializer owampd process return a bad exit code
        """
        cmd = self.owamp_executable + " -c "+ self.server_config_dir
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
    
