from serial import Serial, SerialException

import time
import sys


class Timeout(Exception):
    """An operation timed out."""


class InvalidParam(Exception):
    """A parameter wasn't valid."""


class Busy(Exception):
    """The transceiver is currently busy."""


class ReceptionError(Exception):
    """A reception wasn't successful."""


class FormatError(Exception):
    """Format is not valid."""


class Transceiver:
    """RN2903 Low-Power Long-Range LoRa Technology Transceiver Module Driver"""

    def __init__(self, serial, poll_interval=0.5):
        self._serial = serial
        self._reception_continuous_mode = False
        self.poll_interval = poll_interval

    def _transmit(self, command):
        self._serial.write((command + '\r\n').encode())

    def _receive(self):
        data = self._serial.readline()
        return data[:-2].decode() if data else ''  # Removes \r\n characters.

    def radio_set(self, parameter, value):
        if isinstance(value, int):
            value = str(value)
        self._transmit('radio set ' + parameter + ' ' + value)
        response = self._receive()
        return True if response == 'ok' else False

    def radio_get(self, parameter):
        self._transmit('radio get ' + parameter)
        response = self._receive()
        if response == 'invalid_param':
            raise InvalidParam
        return response

    def mac_pause(self):
        self._transmit('mac pause')
        return int(self._receive())

    def radio_tx(self, data):
        """Transmits a data packet through the radio module.

        <data> is the hexadecimal value representing the data to be
        transmitted.
        """
        self._transmit('radio tx ' + data)

        response = self._receive()  # First response.
        if response == 'invalid_param':
            raise InvalidParam
        if response == 'busy':
            raise Busy

        response = self._receive()  # Second response.
        return True if response == 'radio_tx_ok' else False

    def radio_rx_listen(self, window_size=0):
        """Puts the transceiver in reception mode.

        """
        self._transmit(f'radio rx {window_size}')

        response = self._receive()  # First response.
        if response == 'invalid_param':
            raise InvalidParam
        if response == 'busy':
            raise Busy

        self._reception_continuous_mode = True if window_size == 0 else False

    def _receive_rx(self):
        data = self._serial.readline()
        if data:
            data = data[:-2].decode()  # Removes \r\n characters

            if data == 'radio_err':
                raise ReceptionError if self._reception_continuous_mode else Timeout

            if 'radio_rx' in data:
                data = data.split()[1]
        return data

    def radio_rx_wait(self, peek=False):
        if peek:
            return self._receive_rx()

        while True:
            data = self._receive_rx()
            if data:
                return data
            time.sleep(self.poll_interval)


if __name__ == "__main__":
    try:
        serial = Serial(port='/dev/ttymxc1', baudrate=57600, timeout=1)
    except SerialException:
        sys.exit(1)

    transceiver = Transceiver(serial)
    try:
        transceiver.radio_set('mod', 'lora')
        transceiver.radio_set('freq', 916800000)
        transceiver.radio_set('pwr', 14)
        transceiver.radio_set('sf', 'sf7')
        transceiver.radio_set('crc', 'on')
        transceiver.radio_set('cr', '4/5')
        transceiver.radio_set('wdt', 0)
        transceiver.radio_set('sync', '12')
        transceiver.radio_set('bw', 125)
        transceiver.mac_pause()

        while True:
            try:
                transceiver.radio_rx_listen()
            except Busy:
                pass
            except InvalidParam:
                pass

            try:
                data = transceiver.radio_rx_wait()
            except ReceptionError:
                pass
            except Timeout:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        serial.close()
    sys.exit(0)
