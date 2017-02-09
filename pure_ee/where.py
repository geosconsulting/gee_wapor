#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 04:43:51 2017
@author: fabio
"""

import ee
import ee.mapclient

ee.Initialize()

elev = ee.Image('srtm90_v4')
cover = ee.Image('MCD12Q1/MCD12Q1_005_2001_01_01').select('Land_Cover_Type_1')
blank = ee.Image(0)

# Where (1 <= cover <= 4) and (elev > 1000), set the output to 1.
output = blank.where(
    cover.lte(4).And(cover.gte(1)).And(elev.gt(1000)),
    1)

# Output contains 0s and 1s.  Mask it with itself to get rid of the 0s.
result = output.mask(output)

ee.mapclient.addToMap(result, {'palette': '00AA00'})

mappa =  ee.mapclient

mappa.centerMap(-113.41842, 40.055489, 6)