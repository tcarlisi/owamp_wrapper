"""
owamp_stats.py
    Owamp Stats
@author: Thomas Carlisi
"""
import shlex

class OwampStats():
    """
    Store statistics about the owmpings
    """
    def __init__(self):
        self.exit_code = 0
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
        self.to_reordering = False


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
        self.from_reordering = False


    def collect_stats(self, exit_code, address, data):

        self.exit_code = exit_code
        self.address = address

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
                self.to_reordering = False
            else:
                self.to_reordering = True

            self.from_addr_from = data[2+11].split()[4]
            self.from_addr_to = data[2+11].split()[6]
            self.from_sid = data[3+11].split()[1]
            self.from_first = data[4+11].split()[1]
            self.from_last = data[5+11].split()[1]
            self.from_pkts_sent = data[6+11].split()[0]
            self.from_pkts_lost = data[6+11].split()[2]
            self.from_pkts_dup = data[6+11].split()[5]
            self.from_ow_del_min = data[7+11].split()[4].split("/")[0]
            self.from_ow_del_med = data[7+11].split()[4].split("/")[1]
            self.from_ow_del_max = data[7+11].split()[4].split("/")[2]
            self.from_ow_jitter = data[8+11].split()[3]
            self.from_hops = data[9+11].split()[2]
            if(data[10+11].startswith("no")):
                self.from_reordering = False
            else:
                self.from_reordering = True
            
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






        
