# -*- coding: utf-8 -*-
from rask_cask import RASK
import unittest


def check(**kwargs):
    function_name = None
    if 'function_name' in kwargs:
        function_name = kwargs.get('function_name')
        del (kwargs['function_name'])

    x = RASK(**kwargs)

    if function_name:
        for function in function_name:
            getattr(x, function)()
    return x


class RASKTests(unittest.TestCase):
    def test_spec_1(self):
        tests = [
            (u'ÁÂÀÄÅÃ Ç ÉÊÈË ÍÎÌÏ Ñ ÓÔÒÖÕ ÚÛÙÜ Ý',
             'aaaaaa c eeee iiii n ooooo uuuu y'),
            (u'Æ', 'a')]
        for test in tests:
            test_case = check(str_nme=test[0], pr_uid=35,
                              function_name=['spec_1'])
            self.assertEqual(test[1], test_case.srch_nme)

    def test_spec_4(self):
        tests = [('ONE (TWO) THREE (FOUR) FIVE', 'ONE FIVE'),
                 ('(ONE) (WAY)', '(ONE) (WAY)'),
                 ('ONE (TWO (THREE) FOUR) FIVE', 'ONE FIVE'),
                 ('(DO NOT REMOVE', '(DO NOT REMOVE'),
                 ('DO NOT) REMOVE', 'DO NOT) REMOVE'),
                 ('DO (NOT (REMOVE) THIS', 'DO THIS'),
                 ('DO (NOT (REMOVE)) THIS)', 'DO')
        ]
        for test in tests:
            test_case = check(str_nme=test[0], pr_uid=35,
                              function_name=['spec_4'])
            self.assertEqual(test[1], test_case.srch_nme)

    def test_spec_7_1(self):
        tests = [("L'''AUTOROUTE", "L'AUTOROUTE"),
                 ("'''XYZ", "'XYZ"),
                 ("XYZ'''", "XYZ'")]
        for test in tests:
            test_case = check(str_nme=test[0], pr_uid=35,
                              function_name=['spec_7_1'])
            self.assertEqual(test[1], test_case.srch_nme)

if __name__ == '__main__':
    unittest.main(verbosity=2)
