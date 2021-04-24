"""
owamp_client.py
    Owamp Client
@author: Thomas Carlisi
"""
import shlex
import threading
from subprocess import Popen, PIPE

from .owamp_stats import OwampStats
from .config_store import Config_store

class OwampClient():
    """
    Launch an owamp ping with the configuration indicated in config.ini
    """
    def __init__(self, address, config_store: Config_store):

        self.address = address                              # the target address of the owping
        self.ip_version = config_store.ip_version           # ip protocol version (0, 4 or 6)
        self.nb_packets = config_store.nb_packets           # nb of packets per stream test
        self.schedule = config_store.schedule               # schedule of stream test
        self.port_range = config_store.port_range           # port range for stream test
        self.dhcp_value = config_store.dhcp_value           # dhcp value for stream test
        self.pfsfile = config_store.pfsfile                 # pfs file to authenticate client
        self.executable = config_store.owping_executable    # owping executable
        self.timeout = config_store.timeout

    def owping(self):
        """
        Execute the owping and return the statistics (as OwampStats object)
        """
        cmd = (
            self.executable + " " + self.address
            + " -c " + str(self.nb_packets)
            + " -i " + self.schedule
            + " -u admin"
            + " -k " + self.pfsfile
            + " -L " + str(self.timeout))
            
            
        if not self.ip_version == 0:
            if self.ip_version == 4:
                cmd += " -4"
            elif self.ip_version == 6:
                cmd += " -6"

        if self.port_range:
            cmd += " -P " + self.port_range

        if self.dhcp_value:
            cmd += " -D " + self.dhcp_value
        


        # Execution of Owping
        process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        exit_code = process.wait()

        # Analalyze statistics
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        owamp_stats = OwampStats()
        owamp_stats.collect_stats(exit_code, self.address, stdout)

        return (owamp_stats, stderr)

