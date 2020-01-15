from unittest import TestCase

from Condition_based import checkWin


class TestCheckWin(TestCase):
    def test_checkWin(self):
        gridrow = [['x', 'x', 'x'], ['', '', ''], ['', '', '']]
        gridcol = [['x', '', ''], ['x', '', ''], ['x', '', '']]
        griddiag = [['x', '', ''], ['', 'x', ''], ['', '', 'x']]
        win = [checkWin(grid) for grid in (gridrow, gridcol, griddiag)]
        self.assertTrue(not False in win)
