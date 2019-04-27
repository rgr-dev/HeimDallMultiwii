import unittest

from HeimdallMultiwii.exeptions import MissingCodeError
from HeimdallMultiwii.multiwii import MultiWii


class TestMultiwii(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._multiwii = MultiWii()

    @classmethod
    def tearDownClass(cls):
        cls._multiwii.close_connection()

    def test_fcb_connection(self):
        port_isopen = self._multiwii.open_connection(115200, '/dev/ttyUSB0')
        self.assertTrue(port_isopen)

    def test_get_fcb_data(self):
        result = self._multiwii.get_fcb_data(101)
        self.assertEqual(['cycleTime', 'i2c_errors_count', 'sensor', 'flag', 'global_conf.currentSet'],
                         list(result.keys()))

    def test_send_single_command(self):
        self.assertTrue(self._multiwii.send_simple_command(205))

   # def test_send_command_with_data(self):




