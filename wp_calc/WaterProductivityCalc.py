# coding: utf-8
import ee
import ee.mapclient
import datetime
import matplotlib.pyplot as plt

class WaterProductivityCalc():

    def __init__(self):
        ee.Initialize()
        L1_AGBPSeasonals = ee.ImageCollection("projects/fao-wapor/L1_AGBP")
        L1_AGBPDekadalSeasonals = ee.ImageCollection("projects/fao-wapor/L1_AGBP250")
        ETaCollection = ee.ImageCollection("projects/fao-wapor/L1_AET")
        AET250 = ee.ImageCollection("users/lpeiserfao/AET250")

        region = [[-25.0, -37.0], [60.0, -41.0],
                  [58.0, 39.0], [-31.0, 38.0],
                  [-25.0, -37.0]]
        VisPar_AGBPy = {"opacity": 0.85, "bands": "b1", "min": 0, "max": 12000,
                        "palette": "f4ffd9,c8ef7e,87b332,566e1b",
                        "region": region}
        VisPar_ETay = {"opacity": 0.85, "bands": "b1", "min": 0, "max": 2000,
                       "palette": "d4ffc6,beffed,79c1ff,3e539f",
                       "region": region}
        VisPar_WPbm = {"opacity": 0.85, "bands": "b1", "min": 0, "max": 1.2,
                       "palette": "bc170f,e97a1a,fff83a,9bff40,5cb326",
                       "region": region}

class L1WaterProductivity(WaterProductivityCalc):

    def __init__(self):
        pass

    def image_selection(self):

        data_start = datetime.datetime(2015, 1, 1)
        data_end = datetime.datetime(2015, 2, 1)

        collAGBPFiltered = collAGBP.filterDate(
            data_start,
            data_end)

        collAETFiltered = collAET.filterDate(
            data_start,
            data_end)

        return collAGBPFiltered, collAETFiltered

    def image_processing(self):

        # Above Ground Biomass Production with masked NoData (pixel < 0)
        L1_AGBPSeasonalMasked = L1_AGBPSeasonals.map(
            lambda lista: lista.updateMask(lista.gte(0)))
        # .multiply(10); the multiplier will need to be
        # applied on net FRAME delivery, not on sample dataset
        L1_AGBPSummedYearly = L1_AGBPSeasonalMasked.sum()

        # Actual Evapotranspiration with valid ETa values (>0 and <254)
        ETaColl1 = AET250.map(
            lambda immagine: immagine.updateMask
            (immagine.lt(254) and (immagine.gt(0))))

        # add image property (days in dekad) as band
        ETaColl2 = ETaColl1.map(
            lambda immagine: immagine.addBands(immagine.metadata('days_in_dk')))

        # get ET value, divide by 10 (as per FRAME spec) to get daily value, and
        # multiply by number of days in dekad summed annuallyS
        ETaColl3 = ETaColl2.map(lambda immagine: immagine.select(
            'b1').divide(10).multiply(immagine.select('days_in_dk'))).sum()

        # scale ETsum from mm/m² to m³/ha for WP calculation purposes
        ETaTotm3 = ETaColl3.multiply(10)

        # calculate biomass water productivity and add to map
        WPbm = L1_AGBPSummedYearly.divide(ETaTotm3)

    def image_visualization(self):

        ee.mapclient.addToMap(WPbm, visparams, 'Annual biomass water productivity')
        ee.mapclient.centerMap(17.75, 10.14, 4)

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.imshow(imag_AGBPy)
        ax1.set_title('AGBP')
        ax1.axis('off')

        ax2 = fig.add_subplot(2, 2, 2)
        ax2.imshow(imag_ETaColl3)
        ax2.set_title('Eta')
        ax2.axis('off')

        ax3 = fig.add_subplot(2, 2, 3)
        ax3.imshow(imag_WPbm)
        ax3.set_title('WP')
        ax3.axis('off')
        plt.show()