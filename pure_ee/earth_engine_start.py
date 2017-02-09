# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 04:59:03 2017

@author: fabio
"""

# Import the Earth Engine Python Package
import ee

# Initialize the Earth Engine object, using the authentication credentials.
ee.Initialize()

# Print the information for an image asset.
image = ee.Image('srtm90_v4')
print(image.getInfo())
