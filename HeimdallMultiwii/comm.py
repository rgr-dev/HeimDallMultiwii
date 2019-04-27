#!/usr/bin/env python3
from HeimdallMultiwii.exeptions import *
from HeimdallMultiwii.mspcommands import MSPMessagesEnum
from HeimdallMultiwii.multiwii import MultiWii

from math import degrees, atan2, radians

__author__ = "Roger Moreno"
__copyright__ = "Copyright 2019"
__credits__ = ["Roger Moreno", ""]
__license__ = "MIT"
__version__ = "1.1.16.dev1"
__maintainer__ = "Roger Moreno"
__email__ = "rgrdevelop@gmail.com"
__status__ = "Development"


class Adapter:
    HMC5883_SCALE = 0.92

    def __init__(self, port, baudrate=115200):
        self.flightcontrolboard = MultiWii()
        self._port = port
        self._baudrate = baudrate
        self._is_on = False

    def connect(self):
        if not self.flightcontrolboard.open_connection(self._baudrate, self._port):
            raise WrongPortError("Can not connect with this port try another one...")
        else:
            self._is_on = True

    def disconnect(self):
        if self._is_on:
            # self.flightcontrolboard.disarm()    # TODO: Pending
            self.flightcontrolboard.close_connection()
            self._is_on = False

    def get_ident(self):
        return self._send_request_message(MSPMessagesEnum.MSP_IDENT.value)

    def get_status(self):
        return self._send_request_message(MSPMessagesEnum.MSP_STATUS.value)

    def get_rawimu(self):
        raw_imu = self._send_request_message(MSPMessagesEnum.MSP_RAW_IMU.value)
        magx = raw_imu['magx']
        magy = raw_imu['magy']
        compass_degrees = self.__get_compass_fixed(magx, magy)
        raw_imu['compass_degrees'] = compass_degrees
        self.__fix_coordinates(raw_imu)
        fixed_angx = self.__fix_angx(raw_imu['accx'])
        raw_imu['accx'] = fixed_angx
        return raw_imu

    def get_original_rawimu(self):
        """
        Raw IMU without changes
        :return: RawIMU message without parse any metrics
        """
        return self._send_request_message(MSPMessagesEnum.MSP_RAW_IMU.value)

    def get_servo(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SERVO.value)

    def get_motor(self):
        return self._send_request_message(MSPMessagesEnum.MSP_MOTOR.value)

    def get_rc(self):
        return self._send_request_message(MSPMessagesEnum.MSP_RC.value)

    def get_rawgps(self):
        gps_data = self._send_request_message(MSPMessagesEnum.MSP_RAW_GPS.value)
        self.__fix_coordinates(gps_data)
        return gps_data

    def get_compgps(self):
        return self._send_request_message(MSPMessagesEnum.MSP_COMP_GPS.value)

    def get_altitude(self):
        return self._send_request_message(MSPMessagesEnum.MSP_ALTITUDE.value)

    def get_attitude(self):
        attitude_data = self._send_request_message(MSPMessagesEnum.MSP_ATTITUDE.value)
        fixed_angx = self.__fix_angx(attitude_data['angx'])
        attitude_data['angx'] = fixed_angx
        return attitude_data

    def get_original_attitude(self):
        return self._send_request_message(MSPMessagesEnum.MSP_ATTITUDE.value)

    def get_analog(self):
        return self._send_request_message(MSPMessagesEnum.MSP_ANALOG.value)

    def get_rctuning(self):
        return self._send_request_message(MSPMessagesEnum.MSP_RC_TUNING.value)

    def get_pid(self):
        return self._send_request_message(MSPMessagesEnum.MSP_PID.value)

    def get_box(self):
        return self._send_request_message(MSPMessagesEnum.MSP_BOX.value)

    def get_misc(self):
        return self._send_request_message(MSPMessagesEnum.MSP_MISC.value)

    def get_motorpins(self):
        return self._send_request_message(MSPMessagesEnum.MSP_MOTOR_PINS.value)

    def get_boxnames(self):
        return self._send_request_message(MSPMessagesEnum.MSP_BOXNAMES.value)

    def get_pidnames(self):
        return self._send_request_message(MSPMessagesEnum.MSP_PIDNAMES.value)

    def get_wp(self):
        return self._send_request_message(MSPMessagesEnum.MSP_WP.value)

    def get_boxids(self):
        return self._send_request_message(MSPMessagesEnum.MSP_BOXIDS.value)

    def get_rcrawimu(self):
        return self._send_request_message(MSPMessagesEnum.MSP_RC_RAW_IMU.value)

    def get_setrawrc(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_RAW_RC.value)

    def get_setrawgps(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_RAW_GPS.value)

    def get_setpid(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_PID.value)

    def get_setbox(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_BOX.value)

    def get_setrctuning(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_RC_TUNING.value)

    def get_setmisc(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_MISC.value)

    def get_resetconf(self):
        return self._send_request_message(MSPMessagesEnum.MSP_RESET_CONF.value)

    def get_setwp(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SET_WP.value)

    def get_switchrcserial(self):
        return self._send_request_message(MSPMessagesEnum.MSP_SWITCH_RC_SERIAL.value)

    def get_isserial(self):
        return self._send_request_message(MSPMessagesEnum.MSP_IS_SERIAL.value)

    def get_debug(self):
        return self._send_request_message(MSPMessagesEnum.MSP_DEBUG.value)

    def _send_request_message(self, cmd):
        if self._is_on:
            msg = self.flightcontrolboard.get_fcb_data(cmd)
            return msg
        else:
            raise ClosedConnectionError("Serial Port not connected!")

    def ACC_calibration(self):
        self.flightcontrolboard.send_simple_command(MSPMessagesEnum.MSP_ACC_CALIBRATION.value)

    def MAG_calibration(self):
        self.flightcontrolboard.send_simple_command(MSPMessagesEnum.MSP_MAG_CALIBRATION.value)

    def drone_ARM(self):
        self.flightcontrolboard.arm()

    def drone_DISARM(self):
        self.flightcontrolboard.disarm()

    def send_rc_signal(self, data):
        self.flightcontrolboard.send_rc_signal(data)

    def can_fly(self):
        return self._is_on

    def listen_message(self):
        return self.flightcontrolboard.readmessage(MSPMessagesEnum.MSP_RAW_IMU.value)

    def __fix_coordinates(self, data):
        latitude_fixed = data['GPS_coord[LAT]']
        longitude_fixed = data['GPS_coord[LON]']
        data['GPS_coord[LAT]'] = latitude_fixed / 10000000
        data['GPS_coord[LON]'] = longitude_fixed / 10000000

    def __fix_angx(self, angx):
        if angx < 0:
            return self.__parse_to_clockwise((angx / 10) + 360)
        elif angx == 0:
            return angx
        else:
            return self.__parse_to_clockwise(angx / 10)

    def __get_compass_fixed(self, magx, magy):
        scaled_x = magx * self.HMC5883_SCALE
        scales_y = magy * self.HMC5883_SCALE
        result_radians = atan2(scaled_x, scales_y)
        return self.__parse_to_clockwise(degrees(result_radians))

    def __parse_to_clockwise(self, degr):
        opisite_degrees = -degr
        return radians(opisite_degrees % 360)
