"""
Pymodbus Synchronous Server with Updating Thread
"""
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

from threading import Thread

import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #


def thread_update_context(c):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    register = 3
    slave_id = 0x00
    address = 110
    while True:
        log.debug("updating the context")
        values = c[slave_id].getValues(register, address, count=5)
        values = [v + 1 for v in values]
        log.debug("new values: " + str(values))
        c[slave_id].setValues(register, address, values)
        time.sleep(5)


def run_updating_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(100, [17]*30),
        co=ModbusSequentialDataBlock(100, [17]*30),
        hr=ModbusSequentialDataBlock(100, [17]*30),
        ir=ModbusSequentialDataBlock(100, [17]*30))
    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '2.2.0'

    x = Thread(target=thread_update_context, args=(context,), daemon=True)
    x.start()

    StartTcpServer(context, identity=identity, address=("localhost", 5020))


if __name__ == "__main__":
    run_updating_server()
