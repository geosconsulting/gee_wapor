import ee

ee.Initialize()

geom = ee.Geometry.Polygon(
    [[[-112.115478515625, 39.60899451189312],
      [-112.1044921875, 38.81737493267723],
      [-111.126708984375, 38.7659965678143],
      [-111.038818359375, 39.59206441884747]]])

# Define years of interest
startYear = 2000
endYear = 2016


# Functions for NDVI calcs
def cloudMask(image):
    # mask areas with surface ref value > 0
    mask = image.select('cfmask').lt(1)
    image = image.mask(mask)
    return image


def applyNdvi(image):
    # calculate ndvi for landsat 7
    ndvi = image.normalizedDifference(['B4', 'B3'])
    # rename band
    ndvi = ndvi.select([0], ['ndvi'])
    # retrieve date of image
    imageDate = image.get('system:time_start')
    # return image with date property
    return ndvi.set('system:time_start', imageDate)


# Import, calculate, and filter NDVI for Landsat 7
ndvi = (
    ee.ImageCollection("LANDSAT/LE7_SR")
        .filterBounds(geom)
        .filterDate(ee.Date.fromYMD(startYear, 1, 1), ee.Date.fromYMD(endYear, 1, 1).advance(1, 'year'))
        .filter(ee.Filter.dayOfYear(182, 273))
        .map(cloudMask)
        .map(applyNdvi)
)

# Create list of years
years = ee.List.sequence(startYear, endYear)


def calculateAnnualMean(year_and_collection):
    # Unpack variable from the input parameter
    year_and_collection = ee.List(year_and_collection)
    year = ee.Number(year_and_collection.get(0))
    _collection = ee.ImageCollection(year_and_collection.get(1))

    start_date = ee.Date.fromYMD(year, 1, 1)
    end_date = start_date.advance(1, 'year')
    return _collection.filterDate(start_date, end_date).mean()


# Create a list of year-collection pairs (i.e. pack the function inputs)
list_of_years_and_collections = years.zip(ee.List.repeat(ndvi, years.length()))

annualNdvi = ee.ImageCollection.fromImages(list_of_years_and_collections.map(calculateAnnualMean))

print(annualNdvi.getInfo())
print('size', annualNdvi.size().getInfo())