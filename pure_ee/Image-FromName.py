# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Initialize Earth Engine.

# <codecell>

from IPython.core.display import Image

import ee

ee.Initialize()

# <markdowncell>

# Load the [SRTM 90m DEM](http://earthengine.google.org/#detail/CGIAR%2FSRTM90_V4).

# <codecell>

image = ee.Image('CGIAR/SRTM90_V4')

# <markdowncell>

# Display an section of the dataset.

# <codecell>

north = 37.0
south = 35.0
east = -111.0
west = -115.0
coords = [[west, north],  # NW
          [west, south],  # SW 
          [east, south],  # SE
          [east, north],  # NE
          [west, north]]  # NW
thumbnailURL = image.getThumbUrl({
    'region': coords,
    'format': 'png',
    'min': 0,
    'max': 3000,
    'size': '500'
  })
Image(url=thumbnailURL)

# <markdowncell>

# Load a Landsat 7 scene.

# <codecell>

image = ee.Image('LANDSAT/L7/LE72300681999227EDC00')

# <markdowncell>

# Display an section of the dataset.

# <codecell>

north = -11.64273+0.1
south = -11.64273-0.1
east = -61.61625+0.1
west = -61.61625-0.1
coords = [[west, north],  # NW
          [west, south],  # SW 
          [east, south],  # SE
          [east, north],  # NE
          [west, north]]  # NW
thumbnailURL = image.getThumbUrl({
    'bands': '40,30,20',
    'region': coords,
    'format': 'png',
    'min': 0,
    'max': 255,
    'size': '500'
  })
Image(url=thumbnailURL)

# <codecell>

image = ee.Image("MOD09GA/MOD09GA_005_2012_03_09")
north = 41
south = 37
east = -102.05
west = -109.05
coords = [[west, north],  # NW
          [west, south],  # SW 
          [east, south],  # SE
          [east, north],  # NE
          [west, north]]  # NW
thumbnailURL = image.getThumbUrl({
    'bands': 'sur_refl_b01,sur_refl_b04,sur_refl_b03',
    'region': coords,
    'format': 'png',
    'min': 0,
    'max': 5000,
    'size': '500'
  })
Image(url=thumbnailURL)

# <codecell>


