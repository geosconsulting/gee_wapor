# coding: utf-8
import ee
import ee.mapclient

ee.Initialize()
L1_AGBPSeasonals = ee.ImageCollection("projects/fao-wapor/L1_AGBP")
ETaCollection = ee.ImageCollection("projects/fao-wapor/L1_AET")
AET250 = ee.ImageCollection("users/lpeiserfao/AET250")

rasterSeason1 = ee.Image(L1_AGBPSeasonals.first())

coordinate = rasterSeason1.get('system:footprint')
#print(coordinate.getInfo())
illo = rasterSeason1.get('system:index'),2
#print(type(illo))
index = rasterSeason1.get('system:index')
#print(index.getInfo())

bande = rasterSeason1.bandNames()
bande.getInfo()

region = [[-25.0, -37.0], [60.0, -41.0], [58.0, 39.0], [-31.0, 38.0], [-25.0, -37.0]]
#print(type(L1_AGBPSeasonals.toList(100).getInfo()))
   
#Above Ground Biomass Production with masked NoData (pixel < 0)
L1_AGBPSeasonalMasked =L1_AGBPSeasonals.map(lambda lista: lista.updateMask(lista.gte(0)))
L1_AGBPSummedYearly = L1_AGBPSeasonalMasked.sum(); #.multiply(10); the multiplier will need to be applied on net FRAME delivery, not on sample dataset

#Actual Evapotranspiration with valid ETa values (>0 and <254)
ETaColl1 = AET250.map(lambda immagine: immagine.updateMask(immagine.lt(254) and (immagine.gt(0))))                                             
                                               
#add image property (days in dekad) as band
ETaColl2 = ETaColl1.map(lambda immagine: immagine.addBands(immagine.metadata('days_in_dk')));

#get ET value, divide by 10 (as per FRAME spec) to get daily value, and multiply by number of days in dekad summed annuallyS
ETaColl3 = ETaColl2.map(lambda immagine: immagine.select('b1').divide(10).multiply(immagine.select('days_in_dk'))).sum()

#scale ETsum from mm/m² to m³/ha for WP calculation purposes
ETaTotm3 = ETaColl3.multiply(10)

#calculate biomass water productivity and add to map
WPbm = L1_AGBPSummedYearly.divide(ETaTotm3)
                       
region = [[-25.0, -37.0], [60.0, -41.0], [58.0, 39.0], [-31.0, 38.0], [-25.0, -37.0]]
visparams = {"opacity":1,"bands":["b1"],"min":0,"max":1.2,"palette":["bc170f","e97a1a","fff83a","9bff40","5cb326"]}

ee.mapclient.addToMap(WPbm, visparams, 'Annual biomass water productivity')
ee.mapclient.centerMap(17.75,10.14,4)
