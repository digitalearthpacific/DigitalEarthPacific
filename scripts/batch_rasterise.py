import geopandas as gpd
from geocube.api.core import make_geocube
import os, os.path

#path = "/home/sachin/GMW_1996_2016/GMW_2007_v2.0.shp"
#path = "/home/sachin/GMW_1996_2016/2007.shp"
#path = "/home/sachin/GMW_1996_2016/GMW_001_GlobalMangroveWatch_2016/01_Data/GMW_2016_v2.shp"
path = "/home/sachin/GMW_1996_2016/2016.shp"
gdf = gpd.read_file(path)

cdf = gpd.read_file("/home/sachin/Projects/notebooks/DigitalEarthPacific/notebooks/pic_bounding_box.geojson")
country_names = cdf['NAME'].tolist()

country_names.remove("Solomons_1")
#country_names.remove("Solomons")
#country_names.remove("FSM")

for country_name in country_names:    
    country = cdf.loc[cdf['NAME'] == country_name]
    clipped = gpd.clip(gdf, country)
    
    out_file = "/home/sachin/tmp/" + country_name.lower() + "_mangrove_2016.tif"
    
    if not os.path.exists(out_file):
        print(country_name)
        try:
            out_grid = make_geocube(
                vector_data=clipped,
                measurements=["pxlval"],
                resolution=(-0.0001, 0.0001),
            )    
            print("Writing GeoTiff...")
            out_grid["pxlval"].rio.to_raster(out_file, windowed=True, compress='LZW') #tiled=True 
            print("Completed: " + country_name)
        except Exception as e:
            print(e)
            pass

#rio cogeo create test.tif test-cog.tif
#rio cogeo validate out.tif
print("Finished.")
