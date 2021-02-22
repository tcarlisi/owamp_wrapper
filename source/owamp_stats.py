"""
owamp_stats.py
    Owamp Stats
@author: Thomas Carlisi
"""
import shlex
from subprocess import Popen, PIPE

class OwampStats():
    """
    Store statistics about the owmpings
    """
    def __init__(self):
        self.exit_code = 0
        self.address = ""
        self.addr_from = ""
        self.addr_to = ""
        self.sid = ""
        self.first = ""
        self.last = ""
        self.pkts_sent = 0
        self.pkts_lost = 0
        self.pkts_dup = 0
        self.ow_del_min = 0
        self.ow_del_med = 0
        self.ow_del_max = 0 
        self.ow_jitter = 0
        self.hops = 0
        self.reordering = False


    def collect_stats(self, exit_code, address, data):

        self.exit_code = exit_code
        self.address = address

        if exit_code == 0:
            data = data.splitlines()

            self.addr_from = data[2].split()[4]
            self.addr_to = data[2].split()[6]
            self.sid = data[3].split()[1]
            self.first = data[4].split()[1]
            self.last = data[5].split()[1]
            self.pkts_sent = data[6].split()[0]
            self.pkts_lost = data[6].split()[2]
            self.pkts_dup = data[6].split()[5]
            self.ow_del_min = data[7].split()[4].split("/")[0]
            self.ow_del_med = data[7].split()[4].split("/")[1]
            self.ow_del_max = data[7].split()[4].split("/")[2]
            self.ow_jitter = data[8].split()[3]
            self.hops = data[9].split()[2]
            if(data[10].startswith("no")):
                self.reordering = False
            else:
                self.reordering = True
            
    def _debug_print_stats(self):
        print("addr from: ", self.addr_from)
        print("addr to: ", self.addr_to)
        print("sid:", self.sid)
        print("first:", self.first)
        print("last:", self.last)
        print("pkts_sent:", self.pkts_sent)
        print("pkts_lost:", self.pkts_lost)
        print("pkts_dup:", self.pkts_dup)
        print("ow_del_min:", self.ow_del_min)
        print("ow_del_med:", self.ow_del_med)
        print("ow_del_max:", self.ow_del_max)
        print("ow_jitter:", self.ow_jitter)
        print("hops:", self.hops)
        print("reordering:", self.reordering)






        
