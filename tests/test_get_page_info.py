# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import get_page_info


class TestGet_page_info(TestCase):
    def test_get_page_info(self):
        j = get_page_info()
        for k, v in j.items():
            print(k)
        assert type(j['version']['number']) is int
        pass
