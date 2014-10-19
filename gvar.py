# -*- coding: utf-8 -*-
"""
----------------------------------------------
全局函数
----------------------------------------------
"""
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)





"""
----------------------------------------------
数据供应商
----------------------------------------------
"""
from vendorwind import VendorWind
from vendorcaihui import VendorCaihui

Vendor=enum('wind','caihui')

def loadvendor(vendor):
    v=None
    
    if vendor==Vendor.wind:
        v=VendorWind()
    elif vendor==Vendor.caihui:
        v=VendorCaihui()
    else:
        pass
    
    return v
    


"""
----------------------------------------------
配置
----------------------------------------------
"""
config_vendor_type = Vendor.wind


"""
Wind帐户信息
"""
config_wind_account='w23205041'
config_wind_password='000000'
config_marketmaker_sleep=0.1