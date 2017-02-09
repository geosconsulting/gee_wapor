#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 04:43:51 2017
@author: fabio
"""

import ee
import ee.mapclient

ee.Initialize()

# Get a download URL for an image.
image = ee.Image('srtm90_v4')
ee.mapclient.addToMap(image, {'min': 0, 'max': 3000})
