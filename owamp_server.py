"""
owamp_server.py
    Owamp Server
@author: Thomas Carlisi
"""
import shlex
from subprocess import Popen, PIPE
import os
import signal

class OwampServer():
    """
    TODO : Doc
    """
    def __init__(self, dir_pid):
        self.dir_pid = dir_pid
        print("OWAMP Server initialization...")

    def launch_owampd(self):
        cmd = "Implementation/executables/owampd -c Implementation/config"
        process = Popen(shlex.split(cmd), stdout=PIPE)
        process.communicate()
        exit_code = process.wait()
        print(exit_code)

    def close_owampd(self):
        with open(self.dir_pid + "/owampd.pid", "r") as f:
            pid = int(f.readlines()[0])
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                print("Err: owapd process not killed")
    
