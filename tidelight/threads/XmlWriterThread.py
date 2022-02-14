import time
from queue import Queue
from threading import Thread

from tidelight import XmlWriter
from tidelight.threads.Command import Command, CommandType


class XmlWriterThread(Thread):
    """Thread responsible for writing to the tide data xml file"""

    def __init__(self, name: str, command_queue: Queue, xml_writer_queue: Queue):
        super().__init__(name=name)
        self.command_queue = command_queue
        self.xml_writer_queue = xml_writer_queue
        self.is_stopping = False
        self.handlers = {
            CommandType.STOP: self.stop
        }

    def run(self):
        while not self.is_stopping:
            if not self.command_queue.empty():
                command = self.command_queue.get()
                self.handle_command(command)

            if not self.xml_writer_queue.empty():
                xml_writer: XmlWriter = self.xml_writer_queue.get()
                xml_writer.write()

            time.sleep(1)

    def stop(self, payload):
        self.is_stopping = True

    def handle_command(self, command: Command):
        self.handlers[command.command_type](command.payload)
