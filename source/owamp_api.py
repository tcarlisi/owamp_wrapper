"""
owamp_api.py
    Owamp API
@author: Thomas Carlisi
"""

from .config_store import Config_store, InputError
from .init_config import InitConfig
from .owamp_server import OwampServer
from .owping_scheduler import OwpingScheduler
from .owamp_stats import OwampStats

class OwampApi():
    """
    An Api for starting an owamp server and an owping scheduler

    ...

    Methods
    -------
    configure(config_filename)
        Get parameters from a config file and configure the owamp sever accordingly

    start_server()
        Start the owamp server
    """
    def __init__(self):
        self.config_store = None
        self.server = None
        self.scheduler = None

    def configure(self, config_filename):
        """
        Get parameters from a config file and configure the owamp sever accordingly

        Parameters
        ----------
        config_filename : str
            the path to the config file
        
        Raises
        ------
        InputError
            If there is an error on the input of the config file
        
        ValueError
            If a wrong type is indicated in the input of the config file
        
        Exception 
            Due to multiple possible errors in the writing of the config files 
            of the owamp project
        """
        try:
            self.config_store = Config_store(config_filename)
        except KeyError as err:
            template = "Error owamp during config file reading: Exception of type {0} occurred:\n{1!r}"
            message = template.format(type(err).__name__, err)
            raise Exception(message) from err
        except ValueError as err:
            template = "Error owamp during config file reading: Exception of type {0} occurred:\n{1!r}"
            message = template.format(type(err).__name__, err)
            raise Exception(message) from err
        except InputError as err:
            template = "Error owamp during config file reading: Exception of type {0} occurred:\n{1!r}"
            message = template.format(type(err).__name__, err.message)
            raise Exception(message) from err

        # Initialize owamp configuration
        try:
            InitConfig(self.config_store).init_config()
        except Exception as err:
            template = "Error owamp during config writing: Exception of type {0} occurred:\n{1!r}"
            message = template.format(type(err).__name__, err)
            raise Exception(message)

    def start_server(self):
        """
        Start the owamp server (the configuration MUST have been done before)

        Raises
        ------
        Exception 
            The configuration has not been done before starting the server
            Or
            Error executing the owamp program
        """
        if not self.config_store:
            raise Exception("Error owamp: the configuration of the server has not been done\n")

        self.server = OwampServer(self.config_store)
        try:
            self.server.launch_owampd()
        except Exception as err:
            template = "Error owamp: Exception of type {0} occurred:\n{1!r}"
            message = template.format(type(err).__name__, err)
            raise Exception(message)


    def stop_server(self):
        """
        Stop the owamp server
        
        Raises
        ------
        Exception 
            The server has to been opened before
        """
        if not self.server:
            raise Exception("Error owamp: the server must be opened to be closed\n")
        self.server.close_owampd()

    def start_owping_scheduler(self, callback, callback_fail):
        """
        Start the owmping scheduler. (the configuration MUST have been done before)
        It executes a ping at a fixed rate.
        (One ping per address in the list)

        If there is no address in config file address_list attribute,
        the scheduler is not lauched an no error is raised. 

        Parameters
        ----------
        callback : function
            The function that must be executed once a ping has finised its execution.
        
        Raises
        ------
        Exception 
            the configuration has not been done
        """
        if not self.config_store:
            raise Exception("Error owamp: the configuration has not been done\n")
        if not callback:
            raise Exception("Error owamp: a callback function must be given\n")
        if not callback_fail:
            raise Exception("Error owamp: a callback_fail function must be given\n")


        if self.config_store.address_list:
            self.scheduler = OwpingScheduler(self.config_store, callback, callback_fail)
            self.scheduler.start_owping_scheduler()   

    def stop_owping_scheduler(self):
        """
        Stop the owmping scheduler.
        """
        if self.scheduler:
            self.scheduler.shutdown_owping_scheduler()