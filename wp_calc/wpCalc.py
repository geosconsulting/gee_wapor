# coding: utf-8
import ee
import ee.mapclient
import matplotlib.pyplot as plt


class WaterProductivityCalc():

    def __init__(self):
        pass


class L1WaterProductivity(WaterProductivityCalc):

    def __init__(self):

        ee.Initialize()

        self.L1_AGBP_seasonal = ee.ImageCollection(
            "projects/fao-wapor/L1_AGBP")

        self.region = [[-25.0, -37.0], [60.0, -41.0],
                       [58.0, 39.0], [-31.0, 38.0],
                       [-25.0, -37.0]]

        self.VisPar_AGBPy = {"opacity": 0.85, "bands": "b1",
                             "min": 0, "max": 12000,
                             "palette": "f4ffd9,c8ef7e,87b332,566e1b",
                             "region": self.region}

        self.VisPar_ETay = {"opacity": 0.85, "bands": "b1",
                            "min": 0, "max": 2000,
                            "palette": "d4ffc6,beffed,79c1ff,3e539f",
                            "region": self.region}

        self.VisPar_WPbm = {"opacity": 0.85, "bands": "b1",
                            "min": 0, "max": 1.2,
                            "palette": "bc170f,e97a1a,fff83a,9bff40,5cb326",
                            "region": self.region}

        self.L1_AGBP_dekadal = ee.ImageCollection(
            "projects/fao-wapor/L1_AGBP250")

        self.L1_ETa_dekadal = ee.ImageCollection(
            "projects/fao-wapor/L1_AET")

        self.L1_AET250 = ee.ImageCollection(
            "users/lpeiserfao/AET250")

    def image_selection(self, start_date, end_date):

        # data_start = datetime.datetime(start_date)
        # data_end = datetime.datetime(end_date)

        #data_start = str(start_date).replace('-', ',')
        #data_end = str(end_date).replace('-', ',')

        data_start = str(start_date)
        data_end = str(end_date)

        collAGBPFiltered = self.L1_AGBP_dekadal.filterDate(
            data_start,
            data_end)

        collAETFiltered = self.L1_AET250.filterDate(
            data_start,
            data_end)

        return collAGBPFiltered, collAETFiltered

    def image_selection_annual(self):

        return self.L1_AGBP_seasonal, self.L1_AET250

    def image_processing(self, L1_AGBP_calc, L1_AET_calc):

        # Above Ground Biomass Production with masked NoData (pixel < 0)
        L1_AGBP_masked = L1_AGBP_calc.map(
            lambda lista: lista.updateMask(lista.gte(0)))
        # .multiply(10); the multiplier will need to be
        # applied on net FRAME delivery, not on sample dataset
        L1_AGBP_summed = L1_AGBP_masked.sum()

        # Actual Evapotranspiration with valid ETa values (>0 and <254)
        ETaColl1 = L1_AET_calc.map(
            lambda immagine: immagine.updateMask
            (immagine.lt(254) and (immagine.gt(0))))

        # add image property (days in dekad) as band
        ETaColl2 = ETaColl1.map(
            lambda immagine: immagine.addBands(immagine.metadata(
                                               'days_in_dk')))

        # get ET value, divide by 10 (as per FRAME spec) to get daily
        # value, and  multiply by number of days in dekad summed annuallyS
        ETaColl3 = ETaColl2.map(lambda immagine: immagine.select(
            'b1').divide(10).multiply(immagine.select('days_in_dk'))).sum()

        # scale ETsum from mm/m² to m³/ha for WP calculation purposes
        ETaTotm3 = ETaColl3.multiply(10)

        # calculate biomass water productivity and add to map
        WPbm = L1_AGBP_summed.divide(ETaTotm3)

        return L1_AGBP_summed, ETaColl3, WPbm

    def image_visualization(self, viz_type, L1_AGBP, ETaColl3, WPbm):

        if viz_type == 'm':
            ee.mapclient.addToMap(WPbm,
                                  self.VisPar_WPbm,
                                  'Annual biomass water productivity')
            ee.mapclient.centerMap(17.75, 10.14, 4)

        elif viz_type == 'c':

            url_thumb_AGBP = L1_AGBP.getThumbUrl(self.VisPar_AGBPy)
            thumb_imag_AGBP = plt.imread(url_thumb_AGBP)

            url_thumb_ETaColl3 = ETaColl3.getThumbUrl(self.VisPar_ETay)
            thumb_imag_ETaColl3 = plt.imread(url_thumb_ETaColl3)

            url_thumb_WPbm = WPbm.getThumbUrl(self.VisPar_WPbm)
            thumb_imag_WPbm = plt.imread(url_thumb_WPbm)

            fig = plt.figure()
            ax1 = fig.add_subplot(2, 2, 1)
            ax1.imshow(thumb_imag_AGBP)
            ax1.set_title('AGBP')
            ax1.axis('off')

            ax2 = fig.add_subplot(2, 2, 2)
            ax2.imshow(thumb_imag_ETaColl3)
            ax2.set_title('Eta')
            ax2.axis('off')

            ax3 = fig.add_subplot(2, 2, 3)
            ax3.imshow(thumb_imag_WPbm)
            ax3.set_title('WP')
            ax3.axis('off')
            plt.show()
