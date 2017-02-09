# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/fabio/.spyder2/.temp.py
"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

 
# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
map = Basemap(projection='ortho', lat_0=12, lon_0=41,
              resolution='l', area_thresh=1000.0)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='coral')
 
plt.show()
