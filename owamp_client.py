"""
owamp_client.py
    Owamp Client
@author: Thomas Carlisi
"""
import shlex
from subprocess import Popen, PIPE

class OwampClient():
    """
    TODO : Doc
    """
    def __init__(self, 
                ip_adrresses, 
                dir_output,
                nb_pkts=100, 
                schedule="0.1e",
                test_port_use=False,
                test_ports="",
                auth_mode ="AEO"):

        self.ip_adrresses = ip_adrresses
        self.dir_output = dir_output
        self.nb_pkts = nb_pkts
        self.schedule = schedule
        self.test_port_use = test_port_use
        self.test_ports = test_ports         # form : "xxx-xxx"
        self.auth_mode = auth_mode           # A = auth, E = enc, O = open
        
        print("OWAMP Client initialization...")

    def owping(self):
        for addr in self.ip_adrresses:
            cmd = (
                "owping " + addr + ":8765"
                + " -p "
                + " -d " + self.dir_output
                #+ " -F output/from.owp"
                #+ " -T output/to.owp"
                + " -c " + str(self.nb_pkts)
                + " -i " + self.schedule
                + " -A " + self.auth_mode)
                
            
            if self.test_port_use:
                cmd += " -P " + self.test_ports

            process = Popen(shlex.split(cmd), stdout=PIPE)
            stdout, errs = process.communicate()
            exit_code = process.wait()
            stdout = stdout.decode("utf-8")
            print(stdout)
            print(exit_code)
