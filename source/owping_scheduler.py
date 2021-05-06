"""
owping_scheduler.py
    Owping scheduler
@author: Thomas Carlisi
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from datetime import datetime

from .owamp_client import OwampClient
from .owamp_stats import OwampStats
from .config_store import Config_store

class OwpingScheduler():
    """
    Scheduler for launching owping to all indicated addresses at a fixed frequency
    """

    def __init__(self, config_store: Config_store, callback: callable, callback_fail: callable,  callback_ping_failed: callable):
        self.config_store = config_store                # config store
        self.callback = callback                        # callback function when job done
        self.callback_fail = callback_fail              # callback function when job failed
        self.callback_ping_failed = callback_ping_failed# callback when ping failed
        self.address_list = config_store.address_list   # address list to ping
        self.schedule = config_store.schedule           # schedule of pings

        executors = {'default': ThreadPoolExecutor(config_store.max_threads)}

        self.scheduler = BackgroundScheduler(executors=executors)   # scheduler
        self.owpingers = []                                         # list of owamp clients

    def start_owping_scheduler(self):
        """
        Start the scheduling of owpings
        """
        self.scheduler.start()
        self.scheduler.add_listener(self._scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._create_owpingers()
        for owpinger in self.owpingers:
            self.scheduler.add_job(owpinger.owping, trigger="interval", max_instances=2, seconds=self.config_store.ping_interval, replace_existing=True, next_run_time=datetime.now())

    def shutdown_owping_scheduler(self):
        """
        Shutdown the scheduler
        """
        self.scheduler.shutdown(wait=True)

    def _scheduler_listener(self, event):
        if event.exception:
            self.callback_fail()
        else:
            owamp_stats = event.retval[0]
            stderr = event.retval[1]
            if owamp_stats.exit_code == 0:
                self.callback(owamp_stats)

            else:
                self.callback_ping_failed(owamp_stats, stderr)

    def _create_owpingers(self):
        for addr in self.address_list:
            owpinger = OwampClient(addr, self.config_store)

            self.owpingers.append(owpinger)

    