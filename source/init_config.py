"""
init_config.py
    Initialize configuration for OWAMP/TWAMP
@author: Thomas Carlisi
"""

import fileinput
from config_store import Config_store

class InitConfig():
    """
    Modify the configuration files of the C owamp implementation
    from the configuration file values of the Dx-agent project
    """
    def __init__(self, config_store: Config_store):
        self.config_store = config_store        # structure containing the config.ini values
    
    def init_config(self):
        """
        Modify the C owamp implementation configuration
        """
        conf_file = self.config_store.server_config_dir + "/owamp-server.conf"
        self._change_config_line(conf_file, "user", self.config_store.user)
        self._change_config_line(conf_file, "group", self.config_store.group)
        self._change_config_line(conf_file, "vardir", self.config_store.dir_pid)
        self._change_config_line(conf_file, "datadir", self.config_store.dir_test)

    def _change_config_line(self, filename, prefix, value):
        try:
            for line in fileinput.input(filename, inplace=1):
                if line.startswith(prefix):
                    new_str = prefix
                    if(len(prefix) >= 15):
                        new_str += " " + value + "\n"
                    elif(len(prefix) >= 7):
                        new_str += "\t" + value + "\n"
                    else:
                        new_str += "\t\t" + value + "\n"
                    line = line.replace(line, new_str)
                print(line, end="")
            fileinput.close()
        except Exception as err:
            message = "configuration initialization failed:  {}\n".format(err)
            raise Exception(message) from err