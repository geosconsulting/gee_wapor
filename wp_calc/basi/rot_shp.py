import sys
from osgeo import ogr
import os
import glob
#import shapefile


def image_export(exp_type, WPbm):

    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    dir_shps = "/media/sf_Fabio/Downloads/water productivity/data/tiles/tiles3"
    os.chdir(dir_shps)
    file_shps = glob.glob("*.shp")
    
    for file_shp in file_shps:
        dataSource = driver.Open(file_shp, 0) # 0 means read-only. 1 means writeable.
        # Check to see if shapefile is found.
        if dataSource is None:
             sys.exit(('Could not open {0}.'.format(file_shp)))
        else:            
            layer = dataSource.GetLayer(0)
            extent = layer.GetExtent()
            nome_file = str(file_shp.split('.')[0])
            print nome_file
            #print "Opened {0} Estensione {1}".format(file_shp,extent)
            primo = extent[0],extent[3]
            #print primo
            secondo = extent[0],extent[2]
            #print secondo
            terzo = extent[1],extent[2]
            #print terzo            
            quarto = extent[1],extent[3]
            #print quarto
            
            cut = []
            cut.append(list(primo))
            cut.append(list(secondo))
            cut.append(list(terzo))
            cut.append(list(quarto))
            print cut
            
            Export_WPbm = {                   
                   "crs": "EPSG:4326",
                   "scale": 250,
                   # "region": self.region}
                   'region': cut}          

    
            #print "Spatial Reference {0}".format(layer.GetSpatialRef())
            #print "Tipo geometria features {0}".format(layer.GetGeomType())
            #num_features = layer.GetFeatureCount()
            #print "Numero features {0}".format(num_features)
        #sf = shapefile.Reader(file_shp) 
        #shapes = sf.shapes() 
        #bbox = shapes[0].bbox # Retrieves the bounding box of the first shape
    
        #print bbox # Will print the bounding box coordinates

image_export('a','pippo')
