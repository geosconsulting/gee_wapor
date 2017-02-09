#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 04:43:51 2017
@author: fabio
"""
import ee
import ee.mapclient

ee.Initialize()

worldPop = ee.ImageCollection("WorldPop/POP")

#originale
#pop2010 = WP_2010.mosaic().select('population').rename('pop2010').set('system:time_start',ee.Date.fromYMD(2010,1,1)); 

WP_HND  = worldPop.filter(ee.Filter.inList('country', ['HND'])).filter(ee.Filter.equals('UNadj', 'no'))
WP_HND_2010 = WP_HND.filter(ee.Filter.equals('year', 2010)).select('population')
pop2010 = WP_HND_2010.mosaic().select('population')

viz = {'min':0.0,
       'max':20, 
       'palette': ['F3FEEE',
                   '00ff04',
                   '075e09',
                   '0000FF',
                   'FDFF92',
                   'FF2700',
                   'FF00E7']};
                     
#ee.mapclient.addToMap(pop2010,viz);
ee.mapclient.addToMap(pop2010,viz)
ee.mapclient.centerMap(-86.627, 14.743,7)