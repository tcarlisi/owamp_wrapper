"""
owamp_api.py
    Owamp API
@author: Thomas Carlisi
"""

from config_store import Config_store, InputError
from init_config import InitConfig
from owamp_server import OwampServer
from owping_scheduler import OwpingScheduler

class OwampApi():
    """
    Api for starting an owamp server and an owping scheduler 
    """
    def __init__(self):
        self.config_store = None
        self.server = None
        self.scheduler = None

    def configure(self):
        """
        Get parameters from config.ini and configure the owamp sever accordingly
        """
        try:
            self.config_store = Config_store()
        except ValueError as err:
            message = "Error owamp: {}".format(err) 
            raise Exception(message) from err
        except InputError as err:
            message = "Error owamp: {}".format(err.message) 
            raise Exception(message) from err

        # Initialize owamp configuration
        try:
            InitConfig(self.config_store).init_config()
        except Exception as err:
            message = "Error owamp: {}".format(err) 
            raise Exception(message)

    def start_server(self):
        """
        Start the owamp server (the configuration MUST have been done before)
        """
        if not self.config_store:
            raise Exception("Error owamp: the configuration of the server has not been done\n")

        self.server = OwampServer(self.config_store.dir_pid)
        try:
            self.server.launch_owampd()
        except Exception as err:
            message = "Error owamp: {}".format(err)
            raise Exception(message)


    def stop_server(self):
        """
        Stop the owamp server
        """
        if not self.server:
            raise Exception("Error owamp: the server must be opened to be closed\n")
        self.server.close_owampd()

    def start_owping_scheduler(self, address_list):
        """
        Start the owmping scheduler (one owping per address in 'adress_list')
        """
        if not address_list:
            raise Exception("Error owamp: the address list for the owping scheduler is empty\n")
        self.scheduler = OwpingScheduler(address_list, self.config_store)
        self.scheduler.start_owping_scheduler()   

    def stop_owping_scheduler():
        """
        Stop the owmping scheduler
        """
        self.scheduler.shutdown_owping_scheduler()
