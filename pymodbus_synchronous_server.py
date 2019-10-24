"""
Pymodbus Synchronous Server Example
"""
from pymodbus.server.sync import StartTcpServer

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.device import ModbusDeviceIdentification

def run_server():
    block = ModbusSequentialDataBlock(100, [255]*5)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    """
    Initialize the server information
    """ 
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.2.0'

    StartTcpServer(context, identity=identity, address=('0.0.0.0', 5020))

if __name__ == "__main__":
    run_server()