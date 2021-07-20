import unittest
import pytest

from status_check import Status_check

class TDDtest(unittest.TestCase):
    status = Status_check()

    def test_status_home(self):
        self.assertEqual(self.status.status_check_home(),True)

    def test_status_upload(self):
        self.assertEqual(self.status.status_check_upload(),True)