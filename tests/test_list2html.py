# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from parseLog import rundbcompare, list2html


class TestList2html(TestCase):
    def test_list2html(self):
        res = rundbcompare()
        #f = open('C:/Users/euroadmin/MasterSlaveComp/dummy.txt','w')
        #f.write(str(res))
        #f = open('C:/Users/euroadmin/MasterSlaveComp/dummy.txt', 'r')
        #res = f.readlines()[0].split(', ')
        #f.close()
        #print(res)
        inlist = []
        for i in res:
            inlist.append(i.strip('\''))
        print(len(res))
        df = list2html(res)
        print(df)
        pass
