# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import filetohtml, updateconf


class TestUpdateconf(TestCase):
    def test_updateconf(self):
        x = filetohtml()
        r = updateconf(x)
        assert r.status_code == 200
        pass
