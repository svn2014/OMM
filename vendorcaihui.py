# -*- coding: utf-8 -*-
from vendors import VendorBase

class VendorCaihui(VendorBase):
    name='Caihui'
    def __init__(self):
        print('Caihui loaded')
        #raise NotImplementedError()