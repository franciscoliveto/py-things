from serial import Serial

import time

def to_bytes(seq):
    """Converts seq to a bytes type"""
    if isinstance(seq, int):
        return bytes(str(seq), 'utf8')
    elif isinstance(seq, str):
        return bytes(seq, 'utf8')
    else: 
        pass

def mac_pause(handler: Serial) -> int:
    command = b'mac pause\r\n'
    handler.write(command)
    response = handler.readline()
    # TODO: serial port timeout
    return int(response)

def radio_set(handler, parameter, value):
    byte_value = to_bytes(value)
    byte_parameter = to_bytes(parameter)
    command = b'radio set ' + byte_parameter + b' ' + byte_value + b'\r\n'
    handler.write(command)
    response = handler.readline()
    if response == b'ok\r\n':
        return True
    elif response == b'invalid_param\r\n':
        return False
    else:
        return False
    print(response) # Just for debugging purpouses.

def radio_get(parameter):
    pass

def radio_receive_packet():
    pass

def radio_transmit_packet(handler: Serial, data) -> bool:
    """Transmits a data packet through the radio module.

    <data> is the hexadecimal value representing the data to be
    transmitted, from 0 to 255 for LoRa modulation.

    'radio tx <data>'

    First response after entering the command:
    ok - if parameter is valid and the transceiver is configured in Transmit mode
    invalid_param - if parameter is not valid
    busy - if the transceiver is currently busy
    Second response after effective transmission:
    radio_tx_ok - if transmission was successful
    radio_err - if transmission was unsuccesful
    """
    d = to_bytes(to_bytes(data).hex())
    # TODO: '125' -> '313235' or '125' -> '4D'?
    command = b'radio tx ' + d + b'\r\n'
    handler.write(command)
    response = handler.readline() # Wait for the first response.
    if response == b'invalid_param\r\n' or response == b'busy\r\n':
        return False
    elif response == b'ok\r\n':
        response = handler.readline() # Wait for the second response.
        if response == b'radio_tx_ok\r\n':
            return True
        elif response == b'radio_err\r\n':
            return False
        else: # Unknown response or empty
            return False
    else: # Unknown response or empty
        return False


handler = Serial('/dev/ttyACM1', baudrate=57600, timeout=5)

radio_set(handler, 'mod', 'lora')
radio_set(handler, 'freq', 916800000)
radio_set(handler, 'pwr', 14)
radio_set(handler, 'sf', 'sf7')
radio_set(handler, 'crc', 'on')
radio_set(handler, 'cr', '4/5')
radio_set(handler, 'wdt', 0)
radio_set(handler, 'sync', '12')
radio_set(handler, 'bw', 125)
mac_pause(handler)

while True:
    radio_transmit_packet(handler, 'hello')
    time.sleep(2)


