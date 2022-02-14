from asyncio import Queue

from tidelight.LocationData.Location import Location
from tidelight.LocationData.TideDataFetcher import TideDataFetcher
from tidelight.threads.TideDataFetchThread import TideDataFetchThread


class ThreadManager:

    def __init__(self):
        self.location = Location('59.908', '10.734')
        self.data_fetcher = TideDataFetcher(self.location)

    def run(self):
        data_fetcher_command_queue = Queue()
        data_fetcher_thread = TideDataFetchThread("data fetcher", data_fetcher_command_queue, self.data_fetcher)
        data_fetcher_thread.start()
