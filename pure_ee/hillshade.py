#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 04:43:51 2017
@author: fabio
"""
import math
import ee
import ee.mapclient

ee.Initialize()

def Radians(img):
  return img.toFloat().multiply(math.pi).divide(180)


def Hillshade(az, ze, slope, aspect):
  """Compute hillshade for the given illumination az, el."""
  azimuth = Radians(ee.Image(az))
  zenith = Radians(ee.Image(ze))
  # Hillshade = cos(Azimuth - Aspect) * sin(Slope) * sin(Zenith) +
  #     cos(Zenith) * cos(Slope)
  return (azimuth.subtract(aspect).cos()
          .multiply(slope.sin())
          .multiply(zenith.sin())
          .add(
              zenith.cos().multiply(slope.cos())))

terrain = ee.Algorithms.Terrain(ee.Image('srtm90_v4'))
slope_img = Radians(terrain.select('slope'))
aspect_img = Radians(terrain.select('aspect'))

# Add 1 hillshade at az=0, el=60.
ee.mapclient.addToMap(Hillshade(0, 60, slope_img, aspect_img))
ee.mapclient.centerMap(-121.767, 46.852, 11)