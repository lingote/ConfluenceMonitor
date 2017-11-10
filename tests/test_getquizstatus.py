# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import getquizstatus


class TestGetquizstatus(TestCase):
    def test_getquizstatus(self):
        df = getquizstatus()
        for k, v in df.items():
            print(k)
        pass
