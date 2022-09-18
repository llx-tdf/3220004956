#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/18 11:17
# @Author  : LLX

import unittest
from main import main_test


class Test(unittest.TestCase):
    def testUnit(self):
        self.assertEqual(main_test(), 1)  # 预测为1


if __name__ == '__main__':
    unittest.main()
