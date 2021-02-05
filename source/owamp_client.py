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
                ip_address,
                ip_version=0, 
                nb_packets=100, 
                schedule="0.1e",
                authentication ="AEO",
                port_range="",
                dhcp_value=""):

        self.ip_address = ip_address
        self.ip_version = ip_version
        self.nb_packets = nb_packets
        self.schedule = schedule
        self.authentication = authentication 
        self.port_range = port_range  
        self.dhcp_value = dhcp_value         
        
        print("OWAMP Client initialization...")

    def owping(self):
        cmd = (
            "../Implementation/executables/bin/owping " + self.ip_address + ":8765"
            # -D Dscp_val
            # - 4 ou -6
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
        owamp_stats._debug_print_stats()
        print(exit_code, "Thread Done")
    
    def owping_thread(self):
        thread = threading.Thread(target=self.owping)
        thread.start()
        return thread

