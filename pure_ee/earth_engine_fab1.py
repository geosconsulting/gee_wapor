# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 05:03:56 2017

@author: fabio
"""

from ee import Image
image = Image('LC8_L1T/LC81910312016217LGN00')
print(image.getInfo())