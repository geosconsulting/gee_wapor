# coding: utf-8
import ee
import datetime
import time
import ee.mapclient as mc
import matplotlib.pyplot as plt
import sys
from osgeo import ogr
import os
import glob


class WaterProductivityCalc(object):
    def __init__(self):
        pass

class L1WaterProductivity(WaterProductivityCalc):

    def __init__(self): #, x=None, y=None

        ee.Initialize()

        self._L1_AGBP_SEASONAL = ee.ImageCollection("projects/fao-wapor/L1_AGBP")
        self._L1_AGBP_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_AGBP250")
        self._L1_ETa_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_AET")
        self._L1_AET250 = ee.ImageCollection("users/lpeiserfao/AET250")
        self._L1_NPP_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_NPP250")

        self.l1_AGBP_calc = self._L1_AGBP_SEASONAL
        self.l1_AET250_calc = self._L1_ETa_DEKADAL
        #self.l1_AGBP_calc = x
        #self.l1_AET250_calc = y

    @property
    def multiply_npp(self):
        return self._L1_AGBP_DEKADAL

    @multiply_npp.setter
    def multiply_npp(self, value):
        self.l1_AET250_calc = self._L1_NPP_DEKADAL.map(
            lambda immagine: immagine.multiply(value))

    @property
    def image_selection(self):
        return self.l1_AGBP_calc, self.l1_AET250_calc

    @image_selection.setter
    def image_selection(self, date_p):

        data_start = str(date_p[0])
        data_end = str(date_p[1])

        collAGBPFiltered = self._L1_AGBP_DEKADAL.filterDate(
            data_start,
            data_end)

        collAETFiltered = self._L1_AET250.filterDate(
            data_start,
            data_end)

        self.l1_AGBP_calc = collAGBPFiltered
        self.l1_AET250_calc = collAETFiltered

moltiplicatore = 1.25
elaborazione = L1WaterProductivity()
elaborazione.multiply_npp
elaborazione.multiply_npp = moltiplicatore
elaborazione.multiply_npp

elaborazione.image_selection
uno, due = elaborazione.image_selection
print uno, due
print uno.size().getInfo()
print due.size().getInfo()

start = "2015-1-1"
end = "2015-1-30"
date_v = [start, end]

elaborazione.image_selection = date_v
tre, quattro = elaborazione.image_selection
print tre.size().getInfo()
print quattro.size().getInfo()

