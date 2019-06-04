#!/usr/bin/env python3

from ast import literal_eval
import time
import serial as pyserial
import struct

from HeimdallMultiwii.constants import CTYPE_PATTERNS
from HeimdallMultiwii.exeptions import MissingCodeError, ResponseParserNotImpl, MWCMessageNotSupported
from HeimdallMultiwii.mspcommands import MSPMessagesEnum


def validate_code(f):
    def __validate_code_wrapper(self, code):
        codes = list(map(int, MSPMessagesEnum))
        if code is None or code not in codes:
            raise MissingCodeError("Please provide message code")
        return f(self, code)

    return __validate_code_wrapper


class MultiWii:
    """
    A class used for serial communication with an MiltiWii compatible FCB (Flight Controller Board)

    ...

    Attributes
    ----------
    serial : serial
        Python serial port extension for receiv and send mesages from/to FCB

    Methods
    -------
    open_connection(serport=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self) -> None:
        self.serial = pyserial.Serial(timeout=1)
        # self.logger = logging.getLogger('simpleExample')

    def __del__(self):
        if self.serial.isOpen():
            self.close_connection()

    def open_connection(self, baud_rate, serport=None):
        """Setup and open serial communication with FCB

        :param serport: Serial port for multiwii connection
        :param baud_rate: BaudRate for multiwii connection
        :return: True if connection was successful established

        :raise: Exception if any serial port is provided
        """
        if serport is None:
            raise Exception("Please provide a Serial Port...")
        self.serial.port = serport
        self.serial.baudrate = baud_rate
        self.serial.bytesize = pyserial.EIGHTBITS
        self.serial.parity = pyserial.PARITY_NONE
        self.serial.stopbits = pyserial.STOPBITS_ONE
        self.serial.write_timeout = 3
        self.serial.xonxoff = False
        self.serial.rtscts = False
        self.serial.dsrdtr = False
        return self._connect()

    def _connect(self):
        """
        Open Serial port for communications
        :return: True if Connection was established
        """
        try:
            wait = 6
            self.serial.open()
            # self.logger.info("Connecting with board on port: " + self.serial.port)
            print("Connecting with board on port: " + self.serial.port)
            for i in range(1, wait):
                # self.logger.info(wait - i)
                time.sleep(1)
        except Exception as error:
            # self.logger.warning("Error opening " + self.serial.port + " port. " + str(error))
            return False
            # self.logger.info("Connection Stablished.")
        print("Connection Stablished.")
        return True

    def close_connection(self):
        """
        Close Serial port
        """
        if self.serial.isOpen():
            # self.logger.info("Closing Connection...")
            self.serial.close()
            # self.logger.info("The connection was closed.")
        # else:
        #     self.logger.info("Connection already closed.")

    def send_simple_command(self, wait, code=None):
        """
        Send Single commands e.g. for calibrate MAG or ACC
        No return response
        :param code: MSP message code
        :param wait: Time to sleep
        :return: True if Evething is OK
        """
        message = self._buildpayload(code)
        self._sendmessage(message)
        time.sleep(wait)
        self.serial.flushInput()
        return True

    @validate_code
    def get_fcb_data(self, code=None):
        """
        Send Request Message to the Multiwii FCB
        :param code: MSP Request
        :return: Miltiwii response dict
        """
        message = self._buildpayload(code)
        self._sendmessage(message)
        return self.readmessage(code)

    def _sendmessage(self, message):
        self.serial.write(message)
        self.serial.flushOutput()

    def readmessage(self, code):
        data = self.__extract_data(code)
        if data:
            try:
                fmt = CTYPE_PATTERNS[code]
            except KeyError:
                self.serial.flushInput()
                raise ResponseParserNotImpl('El mensaje no puede ser parseado')
            if fmt == 'PENDING':
                self.serial.flushInput()
                raise ResponseParserNotImpl('El mensaje no puede ser parseado')
            msg = struct.unpack('<' + fmt, data)
            self.serial.flushInput()
            return self._process_message(code, msg)

    def __extract_data(self, code):
        data = b''
        try:
            header = tuple(self.serial.read(3))
            datalength = struct.unpack('<b', self.serial.read())[0]
            struct.unpack('<b', self.serial.read())
            if header == (0x24, 0x4d, 0x3e) and 0x21 not in header:
                data = self.serial.read(datalength)
            elif 0x21 in header:
                self.serial.flushInput()
                raise MWCMessageNotSupported("The board can't response the message {0}".format(code))
            return data
        except (pyserial.serialutil.SerialException, struct.error):
            return data

    # def _flush(self):
    #     self.serial.flushInput()
    #     self.serial.flushOutput()

    def _buildpayload(self, code: int, size: int = 0, data: list = []):
        payload = bytes()
        total_data = [ord('$'), ord('M'), ord('<'), size, code] + data
        if code == MSPMessagesEnum.MSP_SET_PID.value:
            payload += struct.pack('<3bBB%db' % len(data), *total_data)
        else:
            payload += struct.pack('<3bBB%dh' % len(data), *total_data)
        data = payload[3:]
        checksum = code
        if len(data) > 0x02:  # cambiar 0x02 a ord(2)
            checksum = 0
            for byte in data:
                checksum ^= byte
        payload += struct.pack("<%s" % "H" if checksum > 0xff else "B", checksum)
        return payload

    def _process_message(self, code, msg):
        message = literal_eval(str(msg))
        template = _MessagesFormats.TEMPLATES[code]
        #  If any teamplate available, return raw message
        if len(template) == 0:
            return msg
        msglist= list(zip(template, message))
        return dict(msglist)

    def arm(self):
        timer = 0
        start = time.time()
        while timer < 0.5:
            data = [1500, 1500, 2000, 1000]
            message = self._buildpayload(MSPMessagesEnum.MSP_SET_RAW_RC.value, 8, data)
            self._sendmessage(message)
            self.serial.flushOutput()
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start = time.time()

    def disarm(self):
        timer = 0
        start = time.time()
        while timer < 0.5:
            data = [1500, 1500, 1000, 1000]
            message = self._buildpayload(MSPMessagesEnum.MSP_SET_RAW_RC.value, 8, data)
            self._sendmessage(message)
            self.serial.flushOutput()
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start = time.time()

    def send_rc_signal(self, data):
        code = MSPMessagesEnum.MSP_SET_RAW_RC.value
        self.only_send_message(code, 8, data)

    def set_pid(self, data):
        code = MSPMessagesEnum.MSP_SET_PID.value
        self.only_send_message(code, 30, data)
        self.serial.flushInput()

    def only_send_message(self, code, size, data):
        message = self._buildpayload(code, size, data)
        self._sendmessage(message)


class _MessagesFormats:

    TEMPLATES = {
        100: ('VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'),
        101: ('cycleTime', 'i2c_errors_count', 'sensor', 'flag', 'global_conf.currentSet'),
        102: ('accx', 'accy', 'accz', 'gyrx', 'gyry', 'gyrz', 'magx', 'magy', 'magz', 'GPS_coord[LAT]', 'GPS_coord[LON]', 'GPS_altitude'),
        103: ('servo1', 'servo2', 'servo3', 'servo4', 'servo5', 'servo6', 'servo7', 'servo8'),
        104: ('motor1', 'motor2', 'motor3', 'motor4', 'motor5', 'motor6', 'motor7', 'motor8'),
        105: ('roll', 'pitch', 'yaw', 'throttle', 'AUX1', 'AUX2', 'AUX3AUX4'),
        106: ('GPS_FIX', 'GPS_numSat', 'GPS_coord[LAT]', 'GPS_coord[LON]', 'GPS_altitude', 'GPS_speed', 'GPS_ground_course'),
        107: ('GPS_distanceToHome', 'GPS_directionToHome', 'GPS_update'),
        108: ('angx', 'angy', 'heading'),
        109: ('EstAlt', 'vario'),
        110: ('vbat', 'intPowerMeterSum', 'rssi', 'amperage'),
        111: ('byteRC_RATE', 'byteRC_EXPO', 'byteRollPitchRate', 'byteYawRate', 'byteDynThrPID', 'byteThrottle_MID', 'byteThrottle_EXPO'),
        112: (),  # Read more
        113: (),  # Read more
        114: ('intPowerTrigger1', 'conf.minthrottle', 'maxthrottle', 'mincommand', 'failsafe_throttle', 'plog.arm', 'plog.lifetime', 'conf.mag_declination', 'conf.vbatscale', 'conf.vbatlevel_warn1', 'conf.vbatlevel_warn2', 'conf.vbatlevel_crit'),
        115: ('motorpin1', 'motorpin2', 'motorpin3', 'motorpin4', 'motorpin5', 'motorpin6', 'motorpin7', 'motorpin8'),
        116: (),  # Return directly
        117: (),  # Return directly
        118: ('wp_no', 'lat', 'lon', 'AltHold', 'heading', 'time to stay', 'nav flag'),
        119: (),  # Return directly
        200: ('roll', 'pitch', 'yaw', 'throttle', 'AUX1', 'AUX2', 'AUX3AUX4')
    }
