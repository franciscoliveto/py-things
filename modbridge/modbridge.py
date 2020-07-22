#!/usr/bin/env python
'''
modbridge.py -- modbus bridge service.

It bridges the gap between the telemetry API and a SCADA system.
'''
import sys
import getopt
import threading
import logging

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (ModbusSequentialDataBlock,
                                ModbusSlaveContext,
                                ModbusServerContext)

import random
import time

version = "0.1.0"

logger = logging.getLogger('modbridge')
logger.setLevel(logging.DEBUG)

# pymodbus_logger = logging.getLogger('pymodbus')
# pymodbus_logger.setLevel(logging.DEBUG)
"""
               Register Type    Function Code
Coils               0               1
Discrete Input      1               2
Input Register      3               4
Holding Register    4               3

Function Code 	Action 	        Table Name
1            	Read 	        Discrete Output Coils
5           	Write single 	Discrete Output Coil
15          	Write multiple 	Discrete Output Coils
2           	Read 	        Discrete Input Contacts
4           	Read 	        Analog Input Registers
3           	Read 	        Analog Output Holding Registers
6              	Write single 	Analog Output Holding Register
16           	Write multiple 	Analog Output Holding Registers
"""

def sync(context):
    """Update Modbus context."""
    random.seed()
    while True:
        values = [random.randint(0, 65535) for i in range(10)]
        for slave_id in range(1, 4):
            context[slave_id].setValues(4, 0, values)
        time.sleep(3)


if __name__ == "__main__":
    def usage():
        """Print usage and exit."""
        sys.stderr.write("""usage: modbridge.py [OPTIONS]

Mandatory arguments to long options are mandatory for short options too.
  -f, --log-file=FILE        logging output file
  -D, --log-level=NUMBER     logging level [0-4] (0 is default)
      --help                 print a usage message and exit
      --version              output version information and exit
""")
        raise SystemExit(0)

    try:
        (options, arguments) = getopt.getopt(
            sys.argv[1:],
            "f:D:",
            ['log-file=', 'debug-level=', 'help', 'version']
        )
    except getopt.GetoptError as msg:
        sys.stderr.write('modbridge.py: ' + str(msg) + '\n')
        raise SystemExit(1)

    logfile = ''
    loglevel = logging.CRITICAL

    for opt, value in options:
        if opt in ('-f', '--log-file'):
            logfile = value
        elif opt == '-D':
            level = {0: logging.CRITICAL,
                     1: logging.ERROR,
                     2: logging.WARNING,
                     3: logging.INFO,
                     4: logging.DEBUG}
            try:
                loglevel = level[int(value)]
            except (ValueError, KeyError):
                sys.stderr.write(
                    'modbridge.py: invalid logging level %s\n' % value
                )
                raise SystemExit(1)
        elif opt == '-N':
            go_background = False
        elif opt == '--help':
            usage()
        elif opt == '--version':
            sys.stderr.write('Version %s\n' % version)
            raise SystemExit(0)

    if arguments:
        sys.stderr.write('modbridge.py: arguments are not required.\n')
        raise SystemExit(1)

    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if logfile:
        file = logging.FileHandler(logfile)
        file.setLevel(loglevel)
        file.setFormatter(fmt)
        logger.addHandler(file)

    console = logging.StreamHandler()
    console.setLevel(loglevel)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # pymodbus_logger.addHandler(console)

    try:
        block = ModbusSequentialDataBlock(0, [0]*10)
        slaves = {
            1: ModbusSlaveContext(di=block, co=block, hr=block, ir=block),
            2: ModbusSlaveContext(di=block, co=block, hr=block, ir=block),
            3: ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
        }
        context = ModbusServerContext(slaves=slaves, single=False)

        t = threading.Thread(target=sync, args=(context,))
        t.daemon = True
        t.start()

        StartTcpServer(context, address=('127.0.0.1', 5020))
    except KeyboardInterrupt:
        sys.stderr.write("modbridge: aborted\n")
