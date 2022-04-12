
from geocube.api.core import make_geocube
import os, os.path

out_file = "test.tif"
if os.path.exists(out_file): os.remove(out_file)

out_grid = make_geocube(
    vector_data="GMW_2007_v2.0.shp",
    measurements=["pxlval"],
    resolution=(-0.0001, 0.0001),
)

print("Writing GeoTiff...")

out_grid["pxlval"].rio.to_raster(out_file, windowed=True, compress='LZW') #tiled=True 

print("Finished.")

#rio cogeo create test.tif test-cog.tif
#rio cogeo validate out.tif
