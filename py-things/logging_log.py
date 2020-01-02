import logging
import sys

from serial import Serial, SerialException


class SerialHandler(logging.StreamHandler):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def emit(self, record):
        msg = self.format(record)
        stream = self.port
        stream.write((msg + '\r\n').encode())


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('/var/log/gateway/app.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

try:
    serial = Serial(port='/dev/ttymxc0', baudrate=115200)
except SerialException:
    pass
serial_handler = SerialHandler(serial)
serial_handler.setLevel(logging.DEBUG)
serial_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(serial_handler)

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
sys.exit(0)
