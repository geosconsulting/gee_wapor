# coding: utf-8
import ee
import datetime
import ee.mapclient


region = [[-25.0, -37.0], [60.0, -41.0],
          [58.0, 39.0], [-31.0, 38.0], [-25.0, -37.0]]
VisPar_AGBPy = {"opacity": 0.85, "bands": "b1", "min": 0, "max":
                12000, "palette": "f4ffd9,c8ef7e,87b332,566e1b",
                "region": region}
VisPar_ETay = {"opacity": 0.85, "bands": "b1", "min": 0, "max":
               2000, "palette": "d4ffc6,beffed,79c1ff,3e539f",
               "region": region}
VisPar_WPbm = {"opacity": 0.85, "bands": "b1", "min": 0, "max": 1.2,
               "palette": "bc170f,e97a1a,fff83a,9bff40,5cb326",
               "region": region}

ee.Initialize()

collAGBP = ee.ImageCollection("projects/fao-wapor/L1_AGBP250")
collAET = ee.ImageCollection("users/lpeiserfao/AET250")

rasterSeason1 = ee.Image(collAGBP.first())
coordinate = rasterSeason1.get('system:footprint')
index = rasterSeason1.get('system:index')


def GEE_calc(agb_pass, aet_pass):

    # Above Ground Biomass Production with masked NoData (pixel < 0)
    L1_AGBPSeasonalMasked = agb_pass.map(
        lambda lista: lista.updateMask(lista.gte(0)))

    # .multiply(10); the multiplier will need to be
    # applied on net FRAME delivery, not on sample dataset
    L1_AGBPSummedYearly = L1_AGBPSeasonalMasked.sum()

    # Actual Evapotranspiration with valid ETa values (>0 and <254)
    ETaColl1 = aet_pass.map(
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

    return WPbm


def selectRastersInput():

    data_start = datetime.datetime(2015, 1, 1)
    data_end = datetime.datetime(2015, 2, 1)

    collAGBPFiltered = collAGBP.filterDate(
        data_start,
        data_end)

    collAETFiltered = collAET.filterDate(
        data_start,
        data_end)

    return collAGBPFiltered, collAETFiltered


def main(args=None):

    # setup_logging()
    # parser = argparse.ArgumentParser(description='WaPOR Dekad Analysis')

    agb = selectRastersInput()[0]
    aet = selectRastersInput()[1]

    wp = GEE_calc(agb, aet)
    ee.mapclient.addToMap(wp, VisPar_WPbm, 'Annual biomass water productivity')
    ee.mapclient.centerMap(17.75, 10.14, 4)

if __name__ == '__main__':
    main()
