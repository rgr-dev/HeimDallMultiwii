#!/usr/bin/env python3
from HeimdallMultiwii.exeptions import *
from HeimdallMultiwii.mspcommands import MSPMessagesEnum
from HeimdallMultiwii.multiwii import MultiWii

__author__ = "Roger Moreno"
__copyright__ = "Copyright 2019"
__credits__ = ["Roger Moreno", ""]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Roger Moreno"
__email__ = "rgrdevelop@gmail.com"
__status__ = "Development"


class Adapter:

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
        return self._send_message(MSPMessagesEnum.MSP_IDENT.value)

    def get_status(self):
        return self._send_message(MSPMessagesEnum.MSP_STATUS.value)

    def get_rawimu(self):
        return self._send_message(MSPMessagesEnum.MSP_RAW_IMU.value)

    def get_servo(self):
        return self._send_message(MSPMessagesEnum.MSP_SERVO.value)

    def get_motor(self):
        return self._send_message(MSPMessagesEnum.MSP_MOTOR.value)

    def get_rc(self):
        return self._send_message(MSPMessagesEnum.MSP_RC.value)

    def get_rawgps(self):
        return self._send_message(MSPMessagesEnum.MSP_RAW_GPS.value)

    def get_compgps(self):
        return self._send_message(MSPMessagesEnum.MSP_COMP_GPS.value)

    def get_altitude(self):
        return self._send_message(MSPMessagesEnum.MSP_ALTITUDE.value)

    def get_attitude(self):
        return self._send_message(MSPMessagesEnum.MSP_ATTITUDE.value)

    def get_analog(self):
        return self._send_message(MSPMessagesEnum.MSP_ANALOG.value)

    def get_rctuning(self):
        return self._send_message(MSPMessagesEnum.MSP_RC_TUNING.value)

    def get_pid(self):
        return self._send_message(MSPMessagesEnum.MSP_PID.value)

    def get_box(self):
        return self._send_message(MSPMessagesEnum.MSP_BOX.value)

    def get_misc(self):
        return self._send_message(MSPMessagesEnum.MSP_MISC.value)

    def get_motorpins(self):
        return self._send_message(MSPMessagesEnum.MSP_MOTOR_PINS.value)

    def get_boxnames(self):
        return self._send_message(MSPMessagesEnum.MSP_BOXNAMES.value)

    def get_pidnames(self):
        return self._send_message(MSPMessagesEnum.MSP_PIDNAMES.value)

    def get_wp(self):
        return self._send_message(MSPMessagesEnum.MSP_WP.value)

    def get_boxids(self):
        return self._send_message(MSPMessagesEnum.MSP_BOXIDS.value)

    def get_rcrawimu(self):
        return self._send_message(MSPMessagesEnum.MSP_RC_RAW_IMU.value)

    def get_setrawrc(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_RAW_RC.value)

    def get_setrawgps(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_RAW_GPS.value)

    def get_setpid(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_PID.value)

    def get_setbox(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_BOX.value)

    def get_setrctuning(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_RC_TUNING.value)

    def get_acccalibration(self):
        return self._send_message(MSPMessagesEnum.MSP_ACC_CALIBRATION.value)

    def get_magcalibration(self):
        return self._send_message(MSPMessagesEnum.MSP_MAG_CALIBRATION.value)

    def get_setmisc(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_MISC.value)

    def get_resetconf(self):
        return self._send_message(MSPMessagesEnum.MSP_RESET_CONF.value)

    def get_setwp(self):
        return self._send_message(MSPMessagesEnum.MSP_SET_WP.value)

    def get_switchrcserial(self):
        return self._send_message(MSPMessagesEnum.MSP_SWITCH_RC_SERIAL.value)

    def get_isserial(self):
        return self._send_message(MSPMessagesEnum.MSP_IS_SERIAL.value)

    def get_debug(self):
        return self._send_message(MSPMessagesEnum.MSP_DEBUG.value)

    def _send_message(self, cmd):
        if self._is_on:
            msg = self.flightcontrolboard.get_fcb_data(cmd)
            return msg
        else:
            raise ClosedConnectionError("Serial Port not connected!")

    def can_fly(self):
        return self._is_on