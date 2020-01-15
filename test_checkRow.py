from unittest import TestCase

from Condition_based import checkWinThree


class TestCheckRow(TestCase):
    def test_checkRow(self):
        self.assertTrue(checkWinThree('x', ['x', 'x'
                                                 '', 'x']))
