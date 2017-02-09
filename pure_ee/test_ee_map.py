import ee
import ee.mapclient

ee.Initialize()

# Print the information for an image asset.
image = ee.Image('LC8_L1T/LC81910312016217LGN00');

# display the map
ee.mapclient.addToMap(image,
                      {'min':6000,'max':18000,
                      'bands':['B4','B3','B2']},
                      "mymap")

ee.mapclient.centerMap(12.3536,41.7686,9);