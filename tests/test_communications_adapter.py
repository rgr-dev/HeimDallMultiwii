import unittest

from HeimdallMultiwii.comm import Adapter


class TestMultiwiiComm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._comm_adapter = Adapter('/dev/ttyUSB0')
        cls._comm_adapter.connect()

    @classmethod
    def tearDownClass(cls):
        cls._comm_adapter.disconnect()

    def test_get_ident(self):
        result = self._comm_adapter.get_ident()
        self.assertEqual(['VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'],
                         list(result.keys()))

    def test_get_status(self):
        result = self._comm_adapter.get_status()
        self.assertEqual(['cycleTime', 'i2c_errors_count', 'sensor', 'flag', 'global_conf.currentSet'],
                         list(result.keys()))

    def test_get_rawimu(self):
        result = self._comm_adapter.get_rawimu()
        self.assertEqual(['accx', 'accy', 'accz', 'gyrx', 'gyry', 'gyrz', 'magx', 'magy', 'magz', 'compass_degrees'],
                         list(result.keys()))

    def test_get_servo(self):
        result = self._comm_adapter.get_servo()
        self.assertEqual(['servo1', 'servo2', 'servo3', 'servo4', 'servo5', 'servo6', 'servo7', 'servo8'],
                         list(result.keys()))

    def test_get_motor(self):
        result = self._comm_adapter.get_motor()
        self.assertEqual(['motor1', 'motor2', 'motor3', 'motor4', 'motor5', 'motor6', 'motor7', 'motor8'],
                         list(result.keys()))

    def test_get_rc(self):
        result = self._comm_adapter.get_rc()
        self.assertEqual(['roll', 'pitch', 'yaw', 'throttle', 'AUX1', 'AUX2', 'AUX3AUX4'],
                         list(result.keys()))

    def test_get_rawgps(self):
        result = self._comm_adapter.get_rawgps()
        self.assertEqual(['GPS_FIX', 'GPS_numSat', 'GPS_coord[LAT]', 'GPS_coord[LON]', 'GPS_altitude', 'GPS_speed', 'GPS_ground_course'],
                         list(result.keys()))

    #@unittest.expectedFailure
    def test_get_compgps(self):
        result = self._comm_adapter.get_compgps()
        self.assertEqual(['GPS_distanceToHome', 'GPS_directionToHome', 'GPS_update'],
                         list(result.keys()))

    def test_get_altitude(self):
        result = self._comm_adapter.get_altitude()
        self.assertEqual(['EstAlt', 'vario'],
                         list(result.keys()))

    def test_get_attitude(self):
        result = self._comm_adapter.get_attitude()
        self.assertEqual(['angx', 'angy', 'heading'],
                         list(result.keys()))

    def test_get_analog(self):
        result = self._comm_adapter.get_analog()
        self.assertEqual(['vbat', 'intPowerMeterSum', 'rssi', 'amperage'],
                         list(result.keys()))

    def test_get_rctuning(self):
        result = self._comm_adapter.get_rctuning()
        self.assertEqual(['byteRC_RATE', 'byteRC_EXPO', 'byteRollPitchRate', 'byteYawRate', 'byteDynThrPID',
                          'byteThrottle_MID', 'byteThrottle_EXPO'],
                         list(result.keys()))

    @unittest.expectedFailure
    def test_get_pid(self):
        result = self._comm_adapter.get_pid()
        self.assertEqual(['VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'],
                         list(result.keys()))

    @unittest.expectedFailure
    def test_get_box(self):
        result = self._comm_adapter.get_box()
        self.assertEqual(['VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'],
                         list(result.keys()))

    def test_get_misc(self):
        result = self._comm_adapter.get_misc()
        self.assertEqual(['intPowerTrigger1', 'conf.minthrottle', 'maxthrottle', 'mincommand',
                          'failsafe_throttle', 'plog.arm', 'plog.lifetime', 'conf.mag_declination',
                          'conf.vbatscale', 'conf.vbatlevel_warn1', 'conf.vbatlevel_warn2', 'conf.vbatlevel_crit'],
                         list(result.keys()))

    def test_get_motorpins(self):
        result = self._comm_adapter.get_motorpins()
        self.assertEqual(['motorpin1', 'motorpin2', 'motorpin3', 'motorpin4',
                          'motorpin5', 'motorpin6', 'motorpin7', 'motorpin8'],
                         list(result.keys()))

    @unittest.expectedFailure
    def test_get_boxnames(self):
        result = self._comm_adapter.get_boxnames()
        self.assertEqual(['VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'],
                         list(result.keys()))

    @unittest.expectedFailure
    def test_get_pidnames(self):
        result = self._comm_adapter.get_pidnames()
        self.assertEqual(['VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'],
                         list(result.keys()))

    @unittest.expectedFailure
    def test_get_wp(self):
            result = self._comm_adapter.get_wp()
            self.assertEqual(['wp_no', 'lat', 'lon', 'AltHold', 'heading', 'time to stay', 'nav flag'],
                             list(result.keys()))

    @unittest.expectedFailure
    def test_get_boxids(self):
        result = self._comm_adapter.get_boxids()
        self.assertEqual(['VERSION', 'MULTITYPE', 'MSP_VERSION', 'capability'],
                         list(result.keys()))

    # def test_setrawrc(self):
    #     result = self._comm_adapter.get_setrawrc()
    #     self.assertEqual(['roll', 'pitch', 'yaw', 'throttle', 'AUX1', 'AUX2', 'AUX3AUX4'],
    #                      list(result.keys()))






