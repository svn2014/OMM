# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 16:04:01 2014

@author: zhangg
"""
#import gvar as g
#d=g.loadvendor(g.Vendor.wind)


#import security as sec
#s1=sec.Security('600001',sec.Exchange.she)
#s2=sec.Security('000001',sec.Exchange.sze)
##s.printme()
#print(s1.code)
#print(s2.code)
#print(sec.Security.code)


#import option as opt
#o=opt.Option('600001', Exchange.she)
#o.checkrisk()
#o.printme()




#from security import Security
#import option as opt
#
#o1=opt.Option('90000373.SH',Security.Exchange.she)
#o1.getinfo()
#o1.getorderbook()
#
#o2=opt.Option('90000374.SH',Security.Exchange.she)
#o2.getinfo()
#o2.getorderbook()

import marketmaker as mm

optioncodes=['90000373.SH','90000374.SH','90000375.SH']
maker =mm.MarketMaker1()
maker.add(optioncodes)
maker.printme()
maker.start()

print('Done')
#import time
#i = 1
#while i <= 10:
#    print(i)
#    i += 1
#    time.sleep(1) # 休眠1秒
