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

# Filter to only include images within the colorado and utah boundaries.
polygon = ee.Geometry.Polygon([[
    [-109.05, 37.0], [-102.05, 37.0], [-102.05, 41.0],   # colorado
    [-109.05, 41.0], [-111.05, 41.0], [-111.05, 42.0],   # utah
    [-114.05, 42.0], [-114.05, 37.0], [-109.05, 37.0]]])

collection = (ee.ImageCollection('LE7_L1T')
                .filterDate(datetime.datetime(2000,4,1),
                            datetime.datetime(2000,7,1))
                .filterBounds(polygon))
 
image1 = collection.median()
image = image1.select('B1','B2','B3')
ee.mapclient.addToMap(image, {'gain': [1.4, 1.4, 1.1]})

ee.mapclient.centerMap(-110, 40, 5)