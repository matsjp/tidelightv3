import logging
import os
import sys
import threading
from queue import Queue
from threading import Thread

import time
from datetime import datetime

from tidelight.LocationData import TideDataFetcher
from tidelight.threads.Command import Command, CommandType
from tidelight.util import get_next_api_run, get_time_in_30s, get_next_time_from, get_next_time_to


class TideDataFetchThread(Thread):
    """Thread responsible for determining when new tide data must be fetched and fetching the data"""
    is_stopping = False

    def __init__(self, name: str, command_queue: Queue, data_fetcher: TideDataFetcher,
                 xml_lock: threading.Lock):
        super().__init__(name=name)
        self.command_queue = command_queue
        self.data_fetcher = data_fetcher
        self.xml_lock = xml_lock
        self.handlers = {
            CommandType.STOP: self.stop
        }

    def run(self):
        next_run = 0
        while not self.is_stopping:
            if next_run < datetime.now().timestamp():
                try:
                    response = self.data_fetcher.fetch(get_next_time_from(), get_next_time_to())
                    if response is None:
                        next_run = get_time_in_30s()
                    else:
                        next_run = get_next_api_run()

                        try:
                            with self.xml_lock:
                                with open("download.xml", "w+") as xml_file:
                                    xml_file.write(response)
                                if os.path.exists("offline.xml"):
                                    os.remove("offline.xml")
                                os.rename("download.xml", "offline.xml")
                        except Exception as e:
                            logging.exception(e)

                except Exception as e:
                    logging.exception("Error occured: %s", sys.exc_info()[0])
                    logging.info('Location release: 30s unknown error')
                    next_run = get_time_in_30s()

            if not self.command_queue.empty():
                command: Command = self.command_queue.get()
                self.handle_command(command)

            time.sleep(1)

    def stop(self, payload):
        self.is_stopping = True

    def handle_command(self, command: Command):
        self.handlers[command.command_type](command.payload)
