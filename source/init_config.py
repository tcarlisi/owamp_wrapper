"""
init_config.py
    Initialize configuratio for OWAMP/TWAMP
@author: Thomas Carlisi
"""

import fileinput

class InitConfig():
    """
    TODO : Doc
    """
    def __init__(self, user, group, dir_pid, dir_test):
        self.user = user
        self.group = group
        self.dir_pid = dir_pid
        self.dir_test = dir_test
        print("OWAMP Config initialization...")
    
    def init_config(self):
        self._change_config_line("../Implementation/config/owampd.conf", "user", self.user)
        self._change_config_line("../Implementation/config/owampd.conf", "group", self.group)
        self._change_config_line("../Implementation/config/owampd.conf", "vardir", self.dir_pid)
        self._change_config_line("../Implementation/config/owampd.conf", "datadir", self.dir_test)

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
            #TODO : check catch and change msg
            print(err)