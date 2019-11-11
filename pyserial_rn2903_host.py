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
    print(response)  # Just for debugging purpouses.


def radio_get(parameter):
    pass


def radio_receive_packet(handler: Serial, window_size: int = 0) -> str:
    """Receives a data packet from the radio module.

    It blocks waiting for a valid data packet. In case of error or time out
    an exception will be raised. If reception was successful an ASCII string 
    containing the hexadecimal representation of the data that was received
    will be returned.
    """
    ws = to_bytes(window_size)
    command = b'radio rx ' + ws + b'\r\n'
    handler.write(command)
    response = handler.readline()  # Wait for the first response.
    if b'busy' in response:
        handler.write(b'sys reset\r\n')
        handler.readline()  # dummy read()
        return ''
        # TODO: raise an exception.
    elif b'invalid_param' in response:
        pass
    elif b'ok' in response:
        while True:
            response = handler.read_all()
            if b'radio_rx' in response:
                data = response.split()[1]
                return data.decode()
            elif b'radio_err' in response:
                # TODO: raise an exception.
                pass
            time.sleep(1)  # TODO: seconds or milliseconds yield?
    else:
        pass


def radio_transmit_packet(handler: Serial, data: str) -> bool:
    """Transmits a data packet through the radio module.

    <data> is the hexadecimal value representing the data to be
    transmitted.
    """
    command = b'radio tx ' + data.encode() + b'\r\n'
    handler.write(command)
    response = handler.readline()  # Wait for the first response.
    if response == b'invalid_param\r\n' or response == b'busy\r\n':
        return False
    elif response == b'ok\r\n':
        response = handler.readline()  # Wait for the second response.
        if response == b'radio_tx_ok\r\n':
            return True
        elif response == b'radio_err\r\n':
            return False
        else:  # Unknown response or empty
            return False
    else:  # Unknown response or empty
        return False


handler = Serial('/dev/ttyACM0', baudrate=57600, timeout=5)

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

"""
n = 16
while True:
    hex_ascii = hex(n)[2:]
    radio_transmit_packet(handler, hex_ascii)
    n = (n % 65536) + 3
    if n < 16:
        n = 16
    time.sleep(30)

"""

frame = '120004A30B002852FD010001070D023F0203000004000005FF00060000'

while True:
    radio_transmit_packet(handler, frame)
    #data = radio_receive_packet(handler)
    time.sleep(30)
