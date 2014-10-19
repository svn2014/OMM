# -*- coding: utf-8 -*-
"""
@author: zhangg
"""

import marketmaker as mm

optioncodes=['90000373.SH','90000374.SH','90000375.SH']
maker =mm.MarketMaker1()
maker.add(optioncodes)
maker.printme()
maker.start()

print('结束')