# -*- coding: utf-8 -*-
from security import Security
from gvar import enum

"""
----------------------------------------------
期权类(证券类):
----------------------------------------------
数据格式：(在vendor中已经根据该格式读入)
*）期权基础数据[[0]，[1]，...[6]]
    [0]=['90000373.SH', '90000374.SH',...]    #代码
    [1]=['50ETF购10月1.50', '50ETF沽10月1.55',...]    #名称
    [2]=[1.5, 1.55,...]   #行权价
    [3]=['c','p',...]   #类型
    [4]=[datetime.datetime(2014, 8, 28, 0, 0, 0, 5000),...]     #合约起始日
    [5]=[datetime.datetime(2014, 10, 22, 0, 0, 0, 5000),...]    #合约到期日
    [6]=[26, 26, ...]   #剩余期限（日）
"""

class Option(Security):    
    #静态：基础数据集合
    OptionType=enum('call','put','exotic')
    OPTIONSET=None
    
    #期权属性
    callput=None
    strikeprice=None
    listeddate=None
    expirydate=None
    lifedays=None
    greeks=None
    
    def __init__(self,code,exchange):
        self.sectype=Security.SecType.option
        self.desc='期权'
        super(Option,self).__init__(code,exchange)
        
    """
    获取证券基础信息
    """
    def getalloptions(self, underlying):
        try:
            #如果之前没有加载过，则加载全部期权信息
            if Option.OPTIONSET == None:
                Option.OPTIONSET=self._datavendor.getoptionset(underlying)
        except:
            print('获取全部期权数据时异常')
    
    
    def getinfo(self):
        try:
            #加载期权基础信息
            self.getalloptions('510050.SH')
            
            #寻找当前匹配code
            codes=Option.OPTIONSET[0]
            idx=codes.index(self.code)
            if idx>=0:
                self.name=Option.OPTIONSET[1][idx]
                self.strikeprice=Option.OPTIONSET[2][idx]
                self.listeddate=Option.OPTIONSET[4][idx]
                self.expirydate=Option.OPTIONSET[5][idx]
                self.lifedays=Option.OPTIONSET[6][idx]
                #option type
                if Option.OPTIONSET[3][idx]=='c':
                    self.callput = Option.OptionType.call
                elif Option.OPTIONSET[3][idx]=='p':
                    self.callput = Option.OptionType.put
                else:
                    self.callput = Option.OptionType.exotic                    
            else:
                print('找不到期权代码: %s' %(self.code))
        except:
            print('获取期权基础数据时异常')
        
    def checkrisk(self):
        self.greeks = Greeks(self)
        
    """
    获取证券订单簿信息
    """
    def getorderbook(self):
        try:
            self._datavendor.getorderbook(self)
        except:
            print('获取期权订单簿数据时异常')

    def onoderbookcallback(self, data):
#        print('callback %s' %(self.code))
        super(Option, self).onoderbookcallback(data)
        
    """
    交易委托
    """
    def comparetradeside(self, side1,side2):
        output=[]
        for s in [side1.upper(),side2.upper()]:
            if s=='BUY' or s=='COVER' or s=='COVERTODAY':
                output.append(1)    #buy
            else:
                output.append(-1)
        
#        print('%s,%s,%s' %(side1,side2,output))
        if output[0]==output[1]:
            return True
        else:
            return False
        
        
    def sendorder(self, code, tradeside, price, volume):
        """
        下单流程
            1. 如果当前无委托单，则
                1.1 如果当前有持仓，则使用平仓挂单
                    否则使用开仓挂单
            2. 如果当前有委托单，则
                2.1 当前委托单与发送单价格一致，则取消
                    否则，先撤销该委托单，重新挂新单
        """
        #查询委托
        orderdata =self._datavendor.queryorder(self.code)
        
        normalorder=None
        if orderdata==None or orderdata[0] == [None]:
            pass
        else:
            #当前存在委托，筛选已报未成交委托
            normalorder=[i for i in range(len(orderdata[1])) if orderdata[1][i] == 'Normal' and orderdata[17][i] == '已报']
            if len(normalorder)==0:
                normalorder=None
        
        if normalorder==None:
            #当前没有委托，查询持仓，如果没有持仓则下单
            positiondata =self._datavendor.queryposition(self.code)
            if positiondata == [] or positiondata==None:
                #无持仓，直接下单
                self._datavendor.sendorder(code, tradeside, price, volume)
            else:
                #检查持仓方向，如果反向则平仓
#                print(positiondata)
                positionside = positiondata[5][0]
                if not self.comparetradeside(positionside,tradeside):
                    #平仓
                    if positionside.upper() == 'BUY':
                        tradeside='sell'
                    elif positionside.upper() == 'SHORT':
                        tradeside='cover'
                    else:
                        pass
                
                #根据新方案交易
                self._datavendor.sendorder(code, tradeside, price, volume)
                
        else:
            #当前存在委托，筛选已报未成交委托
#            normalorder=[i for i in range(len(orderdata[1])) if orderdata[1][i] == 'Normal']
            for i in normalorder:
                orderno=orderdata[0][i]
                orderside=orderdata[4][i]
                orderprice=orderdata[5][i]
                
#                print('现有委托: %s,%s,%s' %(orderno, orderside, orderprice))
#                print('新增委托: %s,%s,%s' %('+', tradeside, price))
                
                if self.comparetradeside(orderside,tradeside):
                    #同向交易
                    if abs(orderprice-price)<0.0001:
                        #委托已存在，且一致，则取消下单
#                        print('相同委托已存在，取消')
                        break   #不可以换作continue
                    else:
                        #委托已存在，不一致，则先撤单
#                        print('同向委托不一致，撤单')
#                        print(orderdata)
                        self._datavendor.cancelorder(orderno)
                        continue                        
                else:
                    #反向交易
                    continue

                #找不到同向同价委托，下单
#                print('无相同委托，下单')
                self._datavendor.sendorder(code, tradeside, price, volume)
    """
    打印
    """
    #Test#
    def printme(self):
        Security.printme(self)
        try:
            print('K=%f, T=%s, t=%s, life=%d' %(self.strikeprice, self.expirydate.strftime('%Y-%m-%d'), self.listeddate.strftime('%Y-%m-%d'),self.lifedays))
        except:
            print('--------------------error here--------------------')
#        print('D=%f, G=%f, V=%f, T=%f, R=%f' %(self.greeks.delta, self.greeks.gamma, self.greeks.vega, self.greeks.theta,self.greeks.rho))
        
     
"""
----------------------------------------------
期权希腊值:
----------------------------------------------
"""
class Greeks:
    delta=None    
    gamma=None
    vega=None
    theta=None
    rho=None
    
    def __init__(self, option):
        self.calculate(option)
    
    def calculate(self,option):
        #Test#
        self.delta=1.1
        self.gamma=1.2
        self.vega=1.3
        self.theta=1.4
        self.rho=1.5