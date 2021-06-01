"""
owamp_stats.py
    Owamp Stats
@author: Thomas Carlisi
"""
import shlex
import os
from atomicwrites import atomic_write

class OwampStats():
    """
    Store statistics about the owmpings
    """
    def __init__(self):
        self.exit_code = 0
        self.ping_success = False
        self.address = ""


        self.to_addr_from = ""
        self.to_addr_to = ""
        self.to_sid = ""
        self.to_first = ""
        self.to_last = ""
        self.to_pkts_sent = 0
        self.to_pkts_lost = 0
        self.to_pkts_dup = 0
        self.to_ow_del_min = 0
        self.to_ow_del_med = 0
        self.to_ow_del_max = 0 
        self.to_ow_jitter = 0
        self.to_hops = 0
        self.to_reordering = 0


        self.from_addr_from = ""
        self.from_addr_to = ""
        self.from_sid = ""
        self.from_first = ""
        self.from_last = ""
        self.from_pkts_sent = 0
        self.from_pkts_lost = 0
        self.from_pkts_dup = 0
        self.from_ow_del_min = 0
        self.from_ow_del_med = 0
        self.from_ow_del_max = 0 
        self.from_ow_jitter = 0
        self.from_hops = 0
        self.from_reordering = 0


    def collect_stats(self, exit_code, address, data):
        """
        Collect stats from owping stdout
        """
        self.exit_code = exit_code
        self.address = address.split(":")[0]

        if exit_code == 0:
            data = data.splitlines()

            self.to_addr_from = data[2].split()[4]
            self.to_addr_to = data[2].split()[6]
            self.to_sid = data[3].split()[1]
            self.to_first = data[4].split()[1]
            self.to_last = data[5].split()[1]
            self.to_pkts_sent = data[6].split()[0]
            self.to_pkts_lost = data[6].split()[2]
            self.to_pkts_dup = data[6].split()[5]
            self.to_ow_del_min = data[7].split()[4].split("/")[0]
            self.to_ow_del_med = data[7].split()[4].split("/")[1]
            self.to_ow_del_max = data[7].split()[4].split("/")[2]
            self.to_ow_jitter = data[8].split()[3]
            self.to_hops = data[9].split()[2]
            if(data[10].startswith("no")):
                self.to_reordering = 0
            else:
                self.to_reordering = data[10].split()[2].split(".")[0]

            j = 11
            while not data[j].startswith("---"):
                j += 1

            self.from_addr_from = data[j].split()[4]
            self.from_addr_to = data[j].split()[6]
            self.from_sid = data[1+j].split()[1]
            self.from_first = data[2+j].split()[1]
            self.from_last = data[3+j].split()[1]
            self.from_pkts_sent = data[4+j].split()[0]
            self.from_pkts_lost = data[4+j].split()[2]
            self.from_pkts_dup = data[4+j].split()[5]
            self.from_ow_del_min = data[5+j].split()[4].split("/")[0]
            self.from_ow_del_med = data[5+j].split()[4].split("/")[1]
            self.from_ow_del_max = data[5+j].split()[4].split("/")[2]
            self.from_ow_jitter = data[6+j].split()[3]
            self.from_hops = data[7+j].split()[2]
            if(data[8+j].startswith("no")):
                self.from_reordering = 0
            else:
                self.from_reordering = data[8+j].split()[2].split(".")[0]

    def write_stats_in_file(self, directory, overwrite=True):
        """
        Write statistics in file "'self.address'.txt" in a given directory
        """
        with atomic_write(directory + "/" + self.address + ".txt", overwrite=True) as f:
            f.write("yes" + os.linesep)
            f.write(self.to_addr_from + os.linesep)
            f.write(self.to_addr_to + os.linesep)
            f.write(self.to_sid + os.linesep)
            f.write(self.to_first + os.linesep)
            f.write(self.to_last + os.linesep)
            f.write(str(self.to_pkts_sent) + os.linesep)
            f.write(str(self.to_pkts_lost) + os.linesep)
            f.write(str(self.to_pkts_dup) + os.linesep)
            f.write(str(self.to_ow_del_min) + os.linesep)
            f.write(str(self.to_ow_del_med) + os.linesep)
            f.write(str(self.to_ow_del_max) + os.linesep)
            f.write(str(self.to_ow_jitter) + os.linesep)
            f.write(str(self.to_hops) + os.linesep)
            f.write(str(self.to_reordering) + os.linesep)

            f.write(self.from_addr_from + os.linesep)
            f.write(self.from_addr_to + os.linesep)
            f.write(self.from_sid + os.linesep)
            f.write(self.from_first + os.linesep)
            f.write(self.from_last + os.linesep)
            f.write(str(self.from_pkts_sent) + os.linesep)
            f.write(str(self.from_pkts_lost) + os.linesep)
            f.write(str(self.from_pkts_dup) + os.linesep)
            f.write(str(self.from_ow_del_min) + os.linesep)
            f.write(str(self.from_ow_del_med) + os.linesep)
            f.write(str(self.from_ow_del_max) + os.linesep)
            f.write(str(self.from_ow_jitter) + os.linesep)
            f.write(str(self.from_hops) + os.linesep)
            f.write(str(self.from_reordering) + os.linesep)

    def write_error_in_file(self, directory, stderr, overwrite=True):
        """
        Write error in file "'self.address'.txt" in a given directory
        """
        with atomic_write(directory + "/" + self.address + ".txt", overwrite=True) as f:   
            error_msg = "no\nOwping for address {addr} did not work".format(addr=self.address)
            error_msg += "\n" + stderr
            f.write(error_msg)

    def _debug_print_stats(self):

        print("Ping TO")

        print("addr from: ", self.to_addr_from)
        print("addr to: ", self.to_addr_to)
        print("sid:", self.to_sid)
        print("first:", self.to_first)
        print("last:", self.to_last)
        print("pkts_sent:", self.to_pkts_sent)
        print("pkts_lost:", self.to_pkts_lost)
        print("pkts_dup:", self.to_pkts_dup)
        print("ow_del_min:", self.to_ow_del_min)
        print("ow_del_med:", self.to_ow_del_med)
        print("ow_del_max:", self.to_ow_del_max)
        print("ow_jitter:", self.to_ow_jitter)
        print("hops:", self.to_hops)
        print("reordering:", self.to_reordering)

        print("Ping FROM")

        print("addr from: ", self.from_addr_from)
        print("addr to: ", self.from_addr_to)
        print("sid:", self.from_sid)
        print("first:", self.from_first)
        print("last:", self.from_last)
        print("pkts_sent:", self.from_pkts_sent)
        print("pkts_lost:", self.from_pkts_lost)
        print("pkts_dup:", self.from_pkts_dup)
        print("ow_del_min:", self.from_ow_del_min)
        print("ow_del_med:", self.from_ow_del_med)
        print("ow_del_max:", self.from_ow_del_max)
        print("ow_jitter:", self.from_ow_jitter)
        print("hops:", self.from_hops)
        print("reordering:", self.from_reordering)






        
