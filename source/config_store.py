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
        self.owamp_executable = conf_server["owamp_executable"] # owamp executable
        self.port = conf_server["port"]                             # server ip
        if not self.owamp_executable:
            self.owamp_executable = self._add_file_to_dir("Implementation/executables/bin/owampd", owamp_dir)

        self.server_config_dir = conf_server["server_config_dir"]   # server configuration directory
        if not self.server_config_dir:
            self.server_config_dir = self._add_file_to_dir("Implementation/config", owamp_dir)

        self.dir_pid = conf_server["dir_pid"]                       # directory that will contain the owampd pid file
        if not self.dir_pid:
            self.dir_pid = self._add_file_to_dir("Implementation/outputs/dir_pid", owamp_dir)

        self.dir_test = conf_server["dir_test"]                     # directory that will contain test temporary files
        if not self.dir_test:
            self.dir_test = self._add_file_to_dir("Implementation/outputs/dir_test", owamp_dir)

        self.user = conf_server["user"]                             # user that will execute the owamp server
        self.group = conf_server["group"]                           # group that will execute the owamp server

        # Client information
        conf_client = config_object["owamp-client"]
        self.owping_executable = conf_client["owping_executable"]   # owping executable
        if not self.owping_executable:
            self.owping_executable = self._add_file_to_dir("Implementation/executables/bin/owping", owamp_dir)

        pfs = conf_client["pfsfile"]
        if not pfs:
            pfs = self._add_file_to_dir("Implementation/config/owamp-server.pfs", owamp_dir)

        if not fnmatch.fnmatch(pfs, '*.pfs'):
            raise InputError("The pfs file must be a valid filename with extension '.pfs' (but it is : {})\n".format(pfs))
        self.pfsfile = pfs                                          # the client pfs file

        # if the address_list is empty, make it equal to None
        # else it is a list of ip (strings)
        self.address_list = conf_client["address_list"]             # list of address list to ping
        self.address_list = self.address_list.split(",") if self.address_list else None

        self.max_threads = 10
        if self.address_list and len(self.address_list) > 10:
            self.max_threads = len(self.address_list)

        self.ping_interval = float(conf_client["ping_interval"])
        ipv = int(conf_client["ip_version"])
        if ipv != 0 and ipv != 4 and ipv != 6:
            raise InputError("The Ip version (in the config.ini file) must be 0, 4 or 6 (but it is : {})\n".format(ipv))
        else:
            self.ip_version = ipv                                   # IP version used by the owping

        nbp = conf_client["nb_packets"]
        if not nbp.isnumeric():
            raise InputError("The packet number (in the config.ini file) must be an integer (but it is : {})\n".format(nbp))
        else:
            self.nb_packets = int(nbp)                              # nb of packets for each test stream

        # Checked by owping program
        self.schedule = conf_client["schedule"]                     # the schedule of the test stream
        
        pr = conf_client["port_range"]
        if not re.fullmatch("^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", pr):
            raise InputError("The port format is not respected : 0-65535 (but it is : {})\n".format(pr))
        else:
            self.port_range = pr                                    # port range for test stream

        # Checked by owping program
        self.dhcp_value = conf_client["dhcp_value"]                 # dhcp value for test stream packets
        self.timeout = float(conf_client["timeout"])
        if not self.timeout:
            self.timeout = 2

    def _add_file_to_dir(self, filename:str, directory:str):

        if(directory.endswith("/")):
            output = directory + filename
        else:
            output = directory + "/" + filename
        return output
    