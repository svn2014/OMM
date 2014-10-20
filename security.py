# -*- coding: utf-8 -*-
from gvar import enum
import gvar as g

"""
----------------------------------------------
证券类：所有证券的基类
----------------------------------------------
"""
class OrderBook:
    bid=None
    ask=None
    bidsize=None
    asksize=None
    pohlc=None  #preclose, open, high, low, close(latest)
    bidasksprd=-1
    bidasksprdpct=-1    
    
    
    time=None
    requestid=None
    code=None
    fields=None
    
    def __init__(self):
        #注意：初始化一定要放在这里，避免误认为静态变量
        self.bid=[0,0,0,0,0]
        self.ask=[0,0,0,0,0]
        self.bidsize=[0,0,0,0,0]
        self.asksize=[0,0,0,0,0]
        self.pohlc=[0,0,0,0,0]
    
    def update(self, requestid, time, code, fields, data):
#        print('orderbook %s' %(self))
        self.fields=fields
        self.requestid=requestid
        self.code=code
        self.time=time
                
        i=0
        for field in fields:            
            self.fitdata(field, data[i][0])
            i+=1
        
        #计算价差
        self.bidasksprd=-1
        self.bidasksprdpct=-1
        if self.ask[0]==0:
            print('订单簿缺少卖1: %s' %(self.code))
            print(ask)
        elif self.bid[0]==0:
            print('订单簿缺少买1: %s' %(self.code))
            print(bid)
        else:
            self.bidasksprd=self.ask[0]-self.bid[0]
            self.bidasksprdpct=self.bidasksprd/self.bid[0]
        
    
    def fitdata(self, field, value):
        if field == 'RT_ASK1':
            self.ask[0]=value
            return
        
        if field == 'RT_BID1':
            self.bid[0]=value
            return
        
        if field == 'RT_ASIZE1':
            self.asksize[0]=value
            return
            
        if field == 'RT_BSIZE1':
            self.bidsize[0]=value
            return
        
        if field == 'RT_PRE_CLOSE':
            self.pohlc[0]=value
            return
        if field == 'RT_OPEN':
            self.pohlc[1]=value
            return
        if field == 'RT_LAST':
            self.pohlc[4]=value
            return
            
    def printme(self):
        print('%s, %s, %s' %(self.requestid, self.code, self.time))
        print(self.ask)
        print(self.asksize)
        print(self.bid)        
        print(self.bidsize)
        print(self.pohlc)
        print('%f,%f' %(self.bidasksprd, self.bidasksprdpct))
        
class Security:
    #静态
    Exchange=enum('she','sze','cfe')
    SecType=enum('stock','index','etf','future','option')

    #数据供应商
    _datavendor=g.loadvendor(g.config_vendor_type)
    
    #证券变量
    code=None
    name=None
    exchange=None
    sectype=None
    desc=None
    orderbook=None
    
    def __init__(self, code, exchange):
        self.code=code
        self.exchange=exchange
        self.getinfo()
        self.orderbook=OrderBook()
    
    """
    获取证券基础信息
    """
    def getinfo(self):
        raise NotImplementedError()
        
    """
    获取证券订单簿信息
    """
    def getorderbook(self):
        raise NotImplementedError()

    def onoderbookcallback(self,data):
        #根据返回的数据更新订单簿
        self.orderbook.update(data.RequestID, data.Times[0], self.code, data.Fields, data.Data)
        
    """
    交易委托
    """
    
        
        
    """
    打印
    """
    def printme(self):
        print('%s,%s,%s,%s' %(self.desc, self.code, self.name, self.exchange))

    