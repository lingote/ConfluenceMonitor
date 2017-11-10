# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import rundbcompare


class TestRundbcompare(TestCase):
    def test_rundbcompare(self):
        res = rundbcompare()
        print(len(res))
        #for i in res:
        #    print(i)
        pass
