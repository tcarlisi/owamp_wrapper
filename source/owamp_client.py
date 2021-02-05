"""
owamp_client.py
    Owamp Client
@author: Thomas Carlisi
"""
import shlex
from owamp_stats import OwampStats
import threading
from subprocess import Popen, PIPE

class OwampClient():
    """
    TODO : Doc
    """
    def __init__(self, 
                address,
                ip_version, 
                nb_packets, 
                schedule,
                authentication,
                port_range,
                dhcp_value):

        self.address = address
        self.ip_version = ip_version
        self.nb_packets = nb_packets
        self.schedule = schedule
        self.authentication = authentication 
        self.port_range = port_range  
        self.dhcp_value = dhcp_value         
        
        print("OWAMP Client initialization...")

    def owping(self):
        print("yop")
        cmd = (
            "../Implementation/executables/bin/owping " + self.address + ":8765"
            + " -c " + str(self.nb_packets)
            + " -i " + self.schedule
            + " -A " + self.authentication)
            
        if not self.ip_version == 0:
            if self.ip_version == 4:
                cmd += " -4"
            elif self.ip_version == 6:
                cmd += " -6"

        if self.port_range:
            cmd += " -P " + self.port_range

        if self.dhcp_value:
            cmd += " -D " + self.dhcp_value


        process = Popen(shlex.split(cmd), stdout=PIPE)
        stdout, errs = process.communicate()
        exit_code = process.wait()
        stdout = stdout.decode("utf-8")

        owamp_stats = OwampStats()
        owamp_stats.collect_stats(stdout)
        print("Exit code:", exit_code)
        return owamp_stats
    
    def owping_thread(self):
        thread = threading.Thread(target=self.owping)
        thread.start()
        return thread

