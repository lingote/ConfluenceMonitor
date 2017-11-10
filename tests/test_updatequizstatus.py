# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import updatequizstatus


class TestUpdatequizstatus(TestCase):
    def test_updatequizstatus(self):
        updatequizstatus(key=u'CZV Gütertransporte', id=3145737)
        updatequizstatus(key=u'CVZ Personentransporte', id=3145739)
        updatequizstatus(key=u'VZV KatC1-D1 Bues-WoMo-7.5t', id=3145735)
        updatequizstatus(key=u'VZV KatD-Car+Bus', id=3145733)
        updatequizstatus(key=u'VZV KatC-LKW', id=3145731)
        self.fail()
