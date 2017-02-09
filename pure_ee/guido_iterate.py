#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 02:10:20 2017

@author: fabio
"""
import ee

ee.Initialize()

def combineImages(image, previous):
    return ee.Image(previous).addBands(ee.Image(image))
 
collection = ee.ImageCollection('MODIS/MOD13Q1').limit(2)
image = collection.iterate(combineImages, ee.Image())
print ee.Image(image).slice(1).bandNames().size().getInfo()