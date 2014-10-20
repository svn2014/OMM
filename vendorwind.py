# -*- coding: utf-8 -*-
import gvar as g
from vendors import VendorBase
from WindPy import w
import time

"""
----------------------------------------------
数据供应：Wind
----------------------------------------------
"""
class VendorWind(VendorBase):
    name='WindPy'    
    _tradeaccid=[0]
    
    def __init__(self):
        try:
            #wind不会重复启动，也无需特别关闭        
            w.start()
            if w.isconnected:
                pass
            else:
                print('打开Wind失败')
        except:
            print('打开Wind时异常')
    
        #启动交易帐户
        if VendorWind._tradeaccid[0]==0:
            self.tradelogon()
        
    """
    ----------------------------------------------
    证券基础信息
    ----------------------------------------------
    """
    def getoptionset(self, underlying):
        dataset=None
        try:
            today=time.strftime('%Y%m%d',time.localtime())
#            print('loading %s' %(underlying))
            options = w.wset("OptionChain","date="+today+";us_code="+underlying+";option_var=;month=全部;call_put=全部;field=option_code,option_name,strike_price,call_put,first_tradedate,last_tradedate,expiredate")
            dataset=options.Data
            #期权类型需要转换：认购=c，认沽=p
            dataset[3]=[s.replace('认购','c').replace('认沽','p') for s in dataset[3]]
        except:
            print('查找期权时异常')
        
        return dataset
        
    """
    ----------------------------------------------
    证券盘口数据
    ----------------------------------------------
    """
    def getorderbook(self, sec):
        reqid=None
        try:
#            print('loading %s' %(underlying))
            data=w.wsq(sec.code, "rt_ask1,rt_bid1,rt_asize1,rt_bsize1,rt_open,rt_pre_close, rt_last", func=sec.onoderbookcallback)
            reqid=data.RequestID
        except:
            print('查找期权时异常')
        
        return reqid
            
    """
    ----------------------------------------------
    交易委托
    ----------------------------------------------
    """
    def tradelogon(self):
        #仅登陆期权帐户
        if self._tradeaccid[0]>0:
            print('已登陆')
            return
            
        acc=[g.config_wind_account+'03']
        acctype=['sho']
        logon=w.tlogon('0000',0,acc,g.config_wind_password, acctype)
        self._tradeaccid=logon.Data[0]
        
        if logon.ErrorCode <0:
            print('登陆失败：%s' %(logon.Data))
        else:
            print('期权交易帐户登陆')
            
    def tradelogout(self):
        logout =w.tlogout(self._tradeaccid)
        if logout.ErrorCode<0:
            print('登出失败：%s' %(logout.Data))
        else:
            print('期权交易帐户登出')
    
    #下单
    def sendorder(self, code, tradeside, price, volume):
        """
        tradeside:
            buy='1'         -买入开仓，证券买入
            short='2'       -卖出开仓
            cover=‘3’       -买入平仓
            sell='4'        -卖出平仓，证券卖出
            covertoday=‘5’  -买入平今
            selltoday='6'   -卖出平今
        """
        t=w.torder(code, tradeside, price, volume, logonid=self._tradeaccid)
        
        if t.ErrorCode < 0:
            print(t.Data)
        else:
            print('>>>>>>>>>>委托成功：%s,%s, %f, %f' %(code, tradeside, price, volume))
            
    def cancelorder(self, orderno):
        c=w.tcancel(orderno,logonid=self._tradeaccid)
        if c.ErrorCode<0:
            print('撤单失败: 单号%s' %(orderno))
            return -1
        else:
            print('>>>>>>>>>>撤单成功: 单号%s' %(orderno))
            return 0
    
    def queryorder(self, code):
        #code=''表示查询所有代码
        dataset=None
        q = w.tquery(2, logonid=self._tradeaccid, windcode=code)
        if q.ErrorCode<0:
            print(code)
            print(q)
        else:
            dataset = q.Data
            
        return dataset
    
    def queryposition(self, code):
        pass
    """
    w.tquery(1, logonid=3, windcode='90000373.SH')
.ErrorCode=0
.Fields=['SecurityCode', 'SecurityName', 'SecurityForzen', 'CostPrice', 'LastPrice', 'TradeSide', 'EnableVolume', 'TodayOpenVolume', 'TotalFloatProfit', 'MoneyType', 'LogonID', 'ErrorCode', 'ErrorMsg']
.Data=[['90000373.SH', '90000373.SH'], ['华夏上证50ETF期权1410认购1.50', '华夏上证50ETF期权1410认购1.50'], [0.0, 0.0], [0.1415, 0.1448], [0.1367, 0.1367], ['Buy', 'Short'], [79.0, 3.0], [79.0, 3.0], [0.0, 0.0], ['CNY', 'CNY'], [3, 3], [0, 0], ['', '']]

    """