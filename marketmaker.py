# -*- coding: utf-8 -*-
from security import Security
import option as opt
import time
import gvar as g

"""
----------------------------------------------
做市商基类:
----------------------------------------------
"""
class MarketMaker:
    name=None
    optionset=[]
    
    def __init__(self):
        self.name='未定义的做市商策略'

    def add(self,codes):
        #options=['90000373.SH','90000374.SH',...]
        for code in codes:
            o=opt.Option(code, Security.Exchange.she)
            o.getinfo()
            self.optionset.append(o)
    
    def printme(self):
        print('======%s======' %(self.name))
        print('该策略涵盖的合约如下：')
        for o in self.optionset:
            o.printme()

    def start(self):
        #启动订单簿更新(异步)
        for o in self.optionset:
            o.getorderbook()
        
        print('正在启动做市商系统...')
        for i in range(3):
            print(3-i)
            time.sleep(1)   #休眠5秒，等待订单簿数据
        
        print('======开始做市======')
        while(1):
            i+=1
            if i%1==0:
                print('running>%s---Ctrl+C可以退出' %(i))
            
            for o in self.optionset:
                self.checkorder(o)
                time.sleep(g.config_marketmaker_sleep) #每做一次查询，休息一下
        
    
    def checkorder(self, option):
        raise NotImplementedError()
"""
----------------------------------------------
做市商策略1(做市商基类):
----------------------------------------------
"""
class MarketMaker1(MarketMaker):
    """
        该做市策略的报价以基准价为中心，
        买入报价为基准价减去买入报价价差，
        卖出报价为基准价加上卖出报价价差。
        报价价差取为某个固定的值，且双边价差取值对称。
    """
    #参数
    c_spread_pct=0.02   #做市发出订单的价差百分比
    c_min_spread=0.001  #做市发出订单的价差最小值
    c_trade_volume=5    #每次交易张数
    
    def __init__(self):
        self.name = '基于持仓的机械做市商策略'
                
    def checkorder(self, option):
        orderspread=option.orderbook.bidasksprd
        orderspreadpct=option.orderbook.bidasksprdpct
        pohlc=option.orderbook.pohlc
        
        #基准价选择顺序：最新成交价，开盘价，昨收盘
        baseprice=0
        if baseprice==0 and pohlc[4]>0:  #最新价，今收盘
            baseprice = pohlc[4]
        if baseprice==0 and pohlc[1]>0:  #开盘价
            baseprice = pohlc[1]
        if baseprice==0 and pohlc[0]>0:  #昨收盘
            baseprice = pohlc[0]
        
        if baseprice==0:
            print('错误：中心价格为0')
        else:
            ask=baseprice*(1+self.c_spread_pct/2)
            bid=baseprice*(1-self.c_spread_pct/2)
#            print('base=%f, ask=%f, bid=%f' %(baseprice, ask, bid))
            if  (orderspreadpct>self.c_spread_pct and orderspread>self.c_min_spread):
#                print('send order %s: ask-%f, bid-%f' %(option.code, ask, bid))                
                #不要采用向量下单
                option.sendorder(option.code, 'short', ask, self.c_trade_volume)
                option.sendorder(option.code, 'buy', bid, self.c_trade_volume)
            else:
#                print('跳过 %s' %(option.code))
                pass