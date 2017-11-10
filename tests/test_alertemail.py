# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import alertemail


class TestAlertemail(TestCase):
    def test_alertemail(self):
        alertemail('whatever')
        pass
