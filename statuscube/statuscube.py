import logging
import serial

logger = logging.getLogger(__name__)

STATE_NONE = 'n'
STATE_WORKING = 'w'
STATE_SUCCESS = 's'
STATE_ERROR = 'e'
STATE_FAULT = 'f'
_STATES_VALID = [STATE_NONE, STATE_WORKING, STATE_SUCCESS, STATE_ERROR, STATE_FAULT]

PIXEL_0 = '0'
PIXEL_1 = '1'
PIXEL_2 = '2'
PIXEL_3 = '3'
PIXEL_4 = '4'
PIXEL_OMNI = 'a'
_PIXELS_REAL = [PIXEL_0, PIXEL_1, PIXEL_2, PIXEL_3, PIXEL_4]
_PIXELS_VALID = _PIXELS_REAL + [PIXEL_OMNI]

ALL_PIXELS = _PIXELS_REAL
NUM_PIXELS = len(ALL_PIXELS)


class StatusCubeError(Exception):
    pass


class StatusCubeInitError(StatusCubeError):
    pass


class StatusCube(object):
    def __init__(self, serial_port):
        self.serial = serial.Serial(port=serial_port, baudrate=115200, bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=5)

        logger.info('Awaiting greeting from statuscube on serial port {}.'.format(serial_port))

        greeting = 'statuscube'
        if self.serial.read(len(greeting)) != greeting:
            raise StatusCubeInitError('No greeting received from statuscube on serial port {}.'.format(serial_port))

    def set_pixel_state(self, pixel, state):
        assert pixel in _PIXELS_VALID
        assert state in _STATES_VALID

        if pixel in _PIXELS_REAL:
            self._write_pixel_state(pixel, state)
        else:
            assert pixel == PIXEL_OMNI
            for pixel in _PIXELS_REAL:
                self._write_pixel_state(pixel, state)

    def _write_pixel_state(self, pixel, state):
        self.serial.write((pixel + state).encode('UTF-8'))
