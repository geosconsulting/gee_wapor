# coding: utf-8
import ee
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
    def __init__(self):

        ee.Initialize()

        self._L1_AGBP_SEASONAL = ee.ImageCollection("projects/fao-wapor/L1_AGBP")
        self._L1_AGBP_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_AGBP250")
        self._L1_ETa_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_AET")
        self._L1_AET250 = ee.ImageCollection("users/lpeiserfao/AET250")


    @property
    def multi_agbp(self):
        print("chiama il getter")
        return self._L1_AGBP_DEKADAL

    @multi_agbp.setter
    def multi_agbp(self, value):
        print("chiama il setter")
        return self._L1_AGBP_DEKADAL.map(
            lambda immagine: immagine.multiply(value))

moltiplicatore = 1.25
elaborazione = L1WaterProductivity()
elaborazione.multi_agbp
elaborazione.multi_agbp = moltiplicatore
elaborazione.multi_agbp


