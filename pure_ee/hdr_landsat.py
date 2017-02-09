#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 04:43:51 2017
@author: fabio
"""

import ee
import ee.mapclient
import datetime

ee.Initialize()

collection = (ee.ImageCollection('LE7_L1T')
                .filterDate(datetime.datetime(2002,11,8),
                            datetime.datetime(2002,11,9))
                )

image = collection.mosaic().select('B3','B2','B1')
ee.mapclient.addToMap(image,{'gain':'1.6,1.4,1.1'},'Land')

#se lo metto prima come negli esempi errore
ee.mapclient.centerMap(-95.73,18.45,9)

elev = ee.Image('srtm90_v4')
mask1 = elev.mask().eq(0).And(image.mask())
mask2 = elev.eq(0).And(image.mask())

ee.mapclient.addToMap(image.mask(mask1), {'gain': 6.0, 'bias': -200}, 
'Water: Masked')

ee.mapclient.addToMap(image.mask(mask2), {'gain': 6.0, 'bias': -200}, 
'Water: Elev 0')
