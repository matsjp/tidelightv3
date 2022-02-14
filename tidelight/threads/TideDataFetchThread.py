import enum
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
from threading import Thread

from tidelight.LocationData import TideDataFetcher
from tidelight.threads.Command import Command, CommandType
from tidelight.util import get_next_api_run, get_time_in_30s, get_next_time_from, get_next_time_to


class TideDataFetchThread(Thread):
    """Thread responsible for determining when new tide data must be fetched and fetching the data"""
    is_stopping = False

    def __init__(self, name: str, command_queue: Queue, data_fetcher: TideDataFetcher):
        super().__init__(name=name)
        self.command_queue = command_queue
        self.data_fetcher = data_fetcher
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
                        reply = TideDataFetchCommand(TideDataFetchCommand.CommandType.NEW_TIDE_DATA, response)
                        self.command_queue.put(reply)
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


@dataclass
class TideDataFetchCommand:
    class CommandType(enum.Enum):
        NEW_TIDE_DATA = enum.auto

    command_type: CommandType
    payload: ...
