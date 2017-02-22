# coding: utf-8
import ee
import matplotlib.pyplot as plt

ee.Initialize()
L1_AGBPSeasonals = ee.ImageCollection("projects/fao-wapor/L1_AGBP")
ETaCollection = ee.ImageCollection("projects/fao-wapor/L1_AET")
AET250 = ee.ImageCollection("users/lpeiserfao/AET250")

region = [[-25.0, -37.0], [60.0, -41.0], [58.0, 39.0], [-31.0, 38.0], [-25.0, -37.0]]
VisPar_AGBPy = {"opacity":0.85,"bands":"b1","min":0,"max":12000,"palette":"f4ffd9,c8ef7e,87b332,566e1b","region":region}
VisPar_ETay = {"opacity":0.85,"bands":"b1","min":0,"max":2000,"palette":"d4ffc6,beffed,79c1ff,3e539f","region":region}
VisPar_WPbm = {"opacity":0.85,"bands":"b1","min":0,"max":1.2,"palette":"bc170f,e97a1a,fff83a,9bff40,5cb326","region":region}
   
#Above Ground Biomass Production with masked NoData (pixel < 0)
L1_AGBPSeasonalMasked =L1_AGBPSeasonals.map(lambda lista: lista.updateMask(lista.gte(0)))
L1_AGBPSummedYearly = L1_AGBPSeasonalMasked.sum(); #.multiply(10); the multiplier will need to be applied on net FRAME delivery, not on sample dataset

url_AGBPSummedYearly = L1_AGBPSummedYearly.getThumbUrl(VisPar_AGBPy)
imag_AGBPy = plt.imread(url_AGBPSummedYearly)
#plt.imshow(imag_AGBPy)
                                               
#Actual Evapotranspiration with valid ETa values (>0 and <254)
ETaColl1 = AET250.map(lambda immagine: immagine.updateMask(immagine.lt(254) and (immagine.gt(0))))                                             
                                               
#add image property (days in dekad) as band
ETaColl2 = ETaColl1.map(lambda immagine: immagine.addBands(immagine.metadata('days_in_dk')));

#get ET value, divide by 10 (as per FRAME spec) to get daily value, and multiply by number of days in dekad summed annuallyS
ETaColl3 = ETaColl2.map(lambda immagine: immagine.select('b1').divide(10).multiply(immagine.select('days_in_dk'))).sum()
url_ETaColl3 = ETaColl3.getThumbUrl(VisPar_ETay)
imag_ETaColl3 = plt.imread(url_ETaColl3)

#scale ETsum from mm/m² to m³/ha for WP calculation purposes
ETaTotm3 = ETaColl3.multiply(10)

#calculate biomass water productivity and add to map
WPbm = L1_AGBPSummedYearly.divide(ETaTotm3)
url_WPbm = WPbm.getThumbUrl(VisPar_WPbm)
imag_WPbm = plt.imread(url_WPbm)
#plt.imshow(imag_WPbm)

fig = plt.figure()

ax1 = fig.add_subplot(2,2,1)
ax1.imshow(imag_AGBPy)
ax1.set_title('AGBP')

ax2 = fig.add_subplot(2,2,2)
ax2.imshow(imag_ETaColl3)
ax2.set_title('Eta')

ax3 = fig.add_subplot(2,2,3)
ax3.imshow(imag_WPbm)
ax3.set_title('WP')

plt.show()


