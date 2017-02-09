## Synopsis

GEE files python version

## Code Example

import datetime
import ee
import ee.mapclient

ee.Initialize()

collection = (ee.ImageCollection('LE7_L1T')
                .filterDate(datetime.datetime(2002,11,1),
                            datetime.datetime(2002,12,1)))
def NDVI(image):
    return image.expression('float(b("B4") - b("B3")) - (b("B4") + b("B3"))')


## Motivation
Project for Wapor FAO

## Installation

--

## Contributors

F.Lana

## License

Apache