"""
owping_scheduler.py
    Owping scheduler
@author: Thomas Carlisi
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from datetime import datetime
from owamp_client import OwampClient
from owamp_stats import OwampStats
from config_store import Config_store
from owping_journal import OwpingJournal

class OwpingScheduler():
    """
    Scheduler for launching owping to all indicated addresses at a fixed frequency
    """

    def __init__(self, address_list, config_store: Config_store):
        self.address_list = address_list        # address list
        self.config_store = config_store        # config store

        # cf. ConfigStore fields for documentation
        self.ip_version = config_store.ip_version
        self.nb_packets = config_store.nb_packets
        self.schedule = config_store.schedule
        self.authentication = config_store.authentication
        self.port_range = "" if config_store.port_range == 0 else config_store.port_range
        self.dhcp_value = "" if config_store.dhcp_value == 0 else config_store.dhcp_value

        self.scheduler = BackgroundScheduler()  # scheduler
        self.owpingers = []                     # list of owamp clients
        self.journal = OwpingJournal()          # owping journal

    def start_owping_scheduler(self):
        """
        Start the scheduling of owpings
        """
        print("Dev: Owmping scheduler started..")
        self.scheduler.start()
        self.scheduler.add_listener(self._scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._create_owpingers()
        for owpinger in self.owpingers:
            self.scheduler.add_job(owpinger.owping, trigger="interval", seconds=20, replace_existing=True, next_run_time=datetime.now())

    def shutdown_owping_scheduler(self):
        """
        Shutdown the scheduler
        """
        self.scheduler.shutdown()

    def _scheduler_listener(self, event):
        if event.exception:
            print("Dev : Job exception.")
        else:
            print("Dev: Job Done.")
            owamp_stats = event.retval
            if owamp_stats.exit_code == 0:
                owamp_stats._debug_print_stats()
                self.journal.add_in_journal(owamp_stats)
                self.journal.print_journal()
                
            else:
                message = "Owping for address {addr} did not work".format(addr=owamp_stats.address)
                print(message)

    def _create_owpingers(self):
        for addr in self.address_list:
            owpinger = OwampClient(addr, self.config_store)

            self.owpingers.append(owpinger)

    