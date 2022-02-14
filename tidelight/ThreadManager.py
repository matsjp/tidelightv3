
import logging

import array
import threading
from asyncio import Queue

from tidelight.LocationData.Location import Location
from tidelight.LocationData.TideDataFetcher import TideDataFetcher
from tidelight.threads.TideDataFetchThread import TideDataFetchThread


class ThreadManager:

    def __init__(self):
        self.xml_lock = threading.Lock()
        self.location = Location()
        self.location.lat = '59.908'
        self.location.lon = '10.734'
        self.data_fetcher = TideDataFetcher(self.location)

    def run(self):
        command_queue = Queue()
        data_fetcher_thread = TideDataFetchThread("data fetcher", command_queue, self.data_fetcher, self.xml_lock)
        data_fetcher_thread.start()
