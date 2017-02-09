#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 04:43:51 2017
@author: fabio
"""
import datetime
import ee
import ee.mapclient

ee.Initialize()

collection = (ee.ImageCollection('LE7_L1T')
                .filterDate(datetime.datetime(2000,4,1),
                            datetime.datetime(2000,7,1)))

image1 = collection.median()

fc = (ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8')
            .filter(ee.Filter().eq('Name','California')))
image2 = image1.clipToCollection(fc)

image = image2.select('B1','B2','B3')
ee.mapclient.addToMap(image, {'gain': [1.4, 1.4, 1.1]})

ee.mapclient.centerMap(-110, 40, 5)