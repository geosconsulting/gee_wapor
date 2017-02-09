#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 08:40:22 2017

@author: fabio
"""

import ee
import ee.mapclient

ee.Initialize()

collection = ee.ImageCollection('MODIS/MCD43A4_NDVI')
lista = collection.toList(10)
#print lista.getInfo()


image = ee.Image('LC8_L1T/LC81910312016217LGN00')
#print image.getInfo()


bandNames = image.bandNames()
print('Band Names: ', bandNames.getInfo())

b1scale = image.select('B1').projection().nominalScale()
print('Band 1 scale: ', b1scale.getInfo())


b8scale = image.select('B8').projection().nominalScale()
print('Band 8 scale: ', b8scale.getInfo())


ndvi = image.normalizedDifference(['B5', 'B4'])

ee.mapclient.addToMap(ndvi,
                      {'min' : -1,
                      "max": 1},
                      "NDVI")

ee.mapclient.centerMap(12.3536,41.7686,9)
