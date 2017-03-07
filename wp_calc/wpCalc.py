# coding: utf-8
import ee
import time
import ee.mapclient
import matplotlib.pyplot as plt
import sys
from osgeo import ogr
import os
import glob
import datetime

class WaterProductivityCalc(object):

    def __init__(self):
        pass

class L1WaterProductivity(WaterProductivityCalc):

    def __init__(self):

        ee.Initialize()

        self._REGION = [[-25.0, -37.0], [60.0, -41.0], [58.0, 39.0], [-31.0, 38.0],  [-25.0, -37.0]]

        # VETTORI
        self.countries = ee.FeatureCollection('ft:1tdSwUL7MVpOauSgRzqVTOwdfy17KDbw-1d9omPw')
        self.wsheds = ee.FeatureCollection('ft:1IXfrLpTHX4dtdj1LcNXjJADBB-d93rkdJ9acSEWK')

        self._L1_AGBP_SEASONAL = ee.ImageCollection("projects/fao-wapor/L1_AGBP")
        self._L1_AGBP_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_AGBP250")
        self._L1_ETa_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_AET")
        self._L1_AET250 = ee.ImageCollection("users/lpeiserfao/AET250")
        self._L1_NPP_DEKADAL = ee.ImageCollection("projects/fao-wapor/L1_NPP250")

        self.l1_AGBP_calc = self._L1_AGBP_SEASONAL
        self.l1_AET250_calc = self._L1_AET250
        
        self.VisPar_AGBPy = {"opacity": 0.85, "bands": "b1",
                             "min": 0, "max": 12000,
                             "palette": "f4ffd9,c8ef7e,87b332,566e1b",
                             "region": self._REGION}

        self.VisPar_ETay = {"opacity": 1, "bands": "b1",
                            "min": 0, "max": 2000,
                            "palette": "d4ffc6,beffed,79c1ff,3e539f",
                            "region": self._REGION}

        self.VisPar_WPbm = {"opacity": 0.85, "bands": "b1",
                            "min": 0, "max": 1.2,
                            "palette": "bc170f,e97a1a,fff83a,9bff40,5cb326",
                            "region": self._REGION}

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

    def image_processing(self, L1_AGBP_calc, L1_AET_calc):

        # Above Ground Biomass Production with masked NoData (pixel < 0)
        L1_AGBP_masked = L1_AGBP_calc.map(lambda lista: lista.updateMask(lista.gte(0)))
        # .multiply(10); the multiplier will need to be
        # applied on net FRAME delivery, not on sample dataset
        L1_AGBP_summed = L1_AGBP_masked.sum()
        
        # Actual Evapotranspiration with valid ETa values (>0 and <254)
        ETaColl1 = L1_AET_calc.map(lambda imm_eta: imm_eta.updateMask
                                   (imm_eta.lt(254) and (imm_eta.gt(0))))

        # add image property (days in dekad) as band
        ETaColl2 = ETaColl1.map(lambda imm_eta2: imm_eta2.addBands(
                                                 imm_eta2.metadata(
                                                 'days_in_dk')))        
        
        # get ET value, divide by 10 (as per FRAME spec) to get daily
        # value, and  multiply by number of days in dekad summed annuallyS
        ETaColl3 = ETaColl2.map(lambda imm_eta3: imm_eta3.select(
            'b1').divide(10).multiply(imm_eta3.select('days_in_dk'))).sum()

        # scale ETsum from mm/m² to m³/ha for WP calculation purposes
        ETaTotm3 = ETaColl3.multiply(10)

        # calculate biomass water productivity and add to map
        WPbm = L1_AGBP_summed.divide(ETaTotm3)

        return L1_AGBP_summed, ETaColl1, ETaColl2, ETaColl3, WPbm

    def map_id_getter(self, wpbm_calc):
        map_id = wpbm_calc.getMapId(self.VisPar_WPbm)
        return map_id

    def generate_ts(self, paese, data_start, data_end):

        justCountry = self.countries.filter(ee.Filter.eq('Country', paese))
        cutPoly = justCountry.geometry()
        cutBoundingBox = cutPoly.bounds(1)

        ETaCollection_filtered = self._L1_ETa_DEKADAL.filterDate(data_start, data_end).filterBounds(cutBoundingBox)

        def getMean(img):
            return img.reduceRegions(cutBoundingBox,
                                     ee.Reducer.mean(),
                                     200)

        ans = ee.FeatureCollection(ETaCollection_filtered.map(getMean)).flatten().aggregate_array('.all').getInfo()

        x_agbp = [x['properties']['mean'] for x in ans]
        print x_agbp
        labels_agbp = [x['id'][:8] for x in ans]
        lables_data = [datetime.datetime.strptime(label, "%Y%m%d").strftime('%Y-%m-%d') for label in labels_agbp]

        plt.plot(x_agbp)
        plt.xticks(range(len(labels_agbp)), lables_data, rotation=90)
        plt.show()

    def generate_arealstats(self, paese, data_start, data_end):

        justCountry = self.countries.filter(ee.Filter.eq('Country', paese))
        cutPoly = justCountry.geometry()
        cutBoundingBox = cutPoly.bounds(1)
        # regione_paese = ee.Geometry(cutPoly.getInfo()).toGeoJSONString()
        # centroid = justCountry.geometry().centroid()

        ETaCollection_filtered = self._L1_ETa_DEKADAL.filterDate(data_start, data_end).filterBounds(cutBoundingBox)

        def getMean(img):
            return img.reduceRegions(cutBoundingBox,
                                     ee.Reducer.mean(),
                                     200)

        ans = ee.FeatureCollection(ETaCollection_filtered.map(getMean)).flatten().aggregate_array('.all').getInfo()

        x_agbp = [x['properties']['mean'] for x in ans]
        print x_agbp
        labels_agbp = [x['id'][:8] for x in ans]
        lables_data = [datetime.datetime.strptime(label, "%Y%m%d").strftime('%Y-%m-%d') for label in labels_agbp]

        plt.plot(x_agbp)
        plt.xticks(range(len(labels_agbp)), lables_data, rotation=90)
        plt.show()


    def image_visualization(self, viz_type, L1_AGBP, ETaColl3, WPbm):

        if viz_type == 'm':

            ee.mapclient.addToMap(WPbm, self.VisPar_WPbm, 'Annual biomass water productivity')
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
            ax2.set_title('ETaColl3')
            ax2.axis('off')

            ax3 = fig.add_subplot(2, 2, 3)
            ax3.imshow(thumb_imag_WPbm)
            ax3.set_title('WPbm')
            ax3.axis('off')

            plt.show()

    def image_export(self, exp_type, WPbm):
        
        driver = ogr.GetDriverByName('ESRI Shapefile')

        dir_shps = "/media/sf_Fabio/Downloads/water productivity/"
        "data/tiles/tiles5"

        os.chdir(dir_shps)
        file_shps = glob.glob("*.shp")

        for file_shp in file_shps:
            dataSource = driver.Open(file_shp, 0)
            if dataSource is None:
                sys.exit(('Could not open {0}.'.format(file_shp)))
            else:
                layer = dataSource.GetLayer(0)
                extent = layer.GetExtent()
                nome_file = str(file_shp.split('.')[0])
                primo = extent[0], extent[3]
                secondo = extent[0], extent[2]
                terzo = extent[1], extent[2]
                quarto = extent[1], extent[3]

                cut = []
                cut.append(list(primo))
                cut.append(list(secondo))
                cut.append(list(terzo))
                cut.append(list(quarto))

                Export_WPbm = {
                    "crs": "EPSG:4326",
                    "scale": 250,
                    'region': cut}

                if exp_type == 'u':
                    try:
                        url_WPbm = WPbm.getDownloadUrl(Export_WPbm)
                        print(url_WPbm)
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise
                elif exp_type == 'd':
                    task = ee.batch.Export.image(WPbm,
                                                 nome_file,
                                                 Export_WPbm)
                    task.start()
                    while task.status()['state'] == 'RUNNING':
                        print 'Running'
                        # Perhaps task.cancel() at some point.
                        time.sleep(1)
                    print 'Done.', task.status()
                elif exp_type == 'a':
                    pass
                elif exp_type == 'g':
                    pass
                elif exp_type == 'n':
                    print("Nun faccio na minchia")
                    pass
