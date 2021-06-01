"""
config_store.py
    Store the config.ini values
@author: Thomas Carlisi
"""

import re 
import fnmatch
import configparser
import os

class InputError(Exception):
    """
    Exception raised for errors in the input.
    """

    def __init__(self, message):
        self.message = message

class Config_store():
    """
    Store the config.ini values
    """
    def __init__(self, config_filename):
        config_object = configparser.ConfigParser()
        config_object.read(config_filename)

        curr_dir = os.path.dirname(os.path.realpath(__file__))
        owamp_dir = os.path.normpath(curr_dir + os.sep + os.pardir)

        # Server information
        conf_server = config_object["owamp-server"]
        # owamp executable
        self.owamp_executable = conf_server["owamp_executable"]

        # server port
        self.port = conf_server["port"]
        if not self.owamp_executable:
            self.owamp_executable = self._add_file_to_dir("Implementation/executables/bin/owampd", owamp_dir)

        # server configuration directory
        self.server_config_dir = conf_server["server_config_dir"]
        if not self.server_config_dir:
            self.server_config_dir = self._add_file_to_dir("Implementation/config", owamp_dir)

         # directory that will contain the owampd pid file
        self.dir_pid = conf_server["dir_pid"]
        if not self.dir_pid:
            self.dir_pid = self._add_file_to_dir("Implementation/outputs/dir_pid", owamp_dir)

        # directory that will contain test temporary files
        self.dir_test = conf_server["dir_test"]
        if not self.dir_test:
            self.dir_test = self._add_file_to_dir("Implementation/outputs/dir_test", owamp_dir)

        # user that will execute the owamp server
        self.user = conf_server["user"]

        # group that will execute the owamp server
        self.group = conf_server["group"]

        ## Client information
        conf_client = config_object["owamp-client"]
        # owping executable
        self.owping_executable = conf_client["owping_executable"]
        if not self.owping_executable:
            self.owping_executable = self._add_file_to_dir("Implementation/executables/bin/owping", owamp_dir)

        # pfs file
        pfs = conf_client["pfsfile"]
        if not pfs:
            pfs = self._add_file_to_dir("Implementation/config/owamp-server.pfs", owamp_dir)

        if not fnmatch.fnmatch(pfs, '*.pfs'):
            raise InputError("The pfs file must be a valid filename with extension '.pfs' (but it is : {})\n".format(pfs))
        self.pfsfile = pfs

        # list of address list to ping
        # if the address_list is empty, make it equal to None
        # else it is a list of ip (strings)
        self.address_list = conf_client["address_list"]
        self.address_list = self.address_list.split(",") if self.address_list else None

        # Max Threads
        self.max_threads = 10
        if self.address_list and len(self.address_list) > 10:
            self.max_threads = len(self.address_list)

        # Ping interval
        self.ping_interval = float(conf_client["ping_interval"])

        # IP version used by the owping
        ipv = conf_client["ip_version"] 
        if ipv:
            ipv = int(ipv)
            if not(ipv == 4 or ipv == 6):
                raise InputError("The Ip version (in the config.ini file) must be 4 or 6 (but it is : {})\n".format(ipv))
            self.ip_version = ipv
        else:
            self.ip_version = 0

        # nb of packets for each test stream
        nbp = conf_client["nb_packets"]
        if not nbp.isnumeric():
            raise InputError("The packet number (in the config.ini file) must be an integer (but it is : {})\n".format(nbp))
        else:
            self.nb_packets = int(nbp)

        # the schedule of the test stream
        self.schedule = conf_client["schedule"]
        
        # port range for test stream
        pr = conf_client["port_range"]
        if pr:
            if not re.fullmatch("^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", pr):
                raise InputError("The port format is not respected : 0-65535 (but it is : {})\n".format(pr))
            self.port_range = pr
        else:
            self.port_range = None

        # dhcp value for test stream packets
        dhcp = conf_client["dhcp_value"]
        if dhcp:
            self.dhcp_value = dhcp
        else:
            self.dhcp_value = None
            
        self.timeout = float(conf_client["timeout"])
        if not self.timeout:
            self.timeout = 2

    def _add_file_to_dir(self, filename:str, directory:str):

        if(directory.endswith("/")):
            output = directory + filename
        else:
            output = directory + "/" + filename
        return output
    