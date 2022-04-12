import numpy as np
import pandas as pd
import xarray as xr
from affine import Affine
from pathlib import Path
import xarray
import matplotlib.pyplot as plt
from azure.storage.blob import ContainerClient
from os import path
from cogeo_mosaic.mosaic import MosaicJSON
from cogeo_mosaic.backends import MosaicBackend
import glob

local_path = "/home/sachin/tmp/cog"

account_url = "https://deppcpublicstorage.blob.core.windows.net/output?sp=racwl&st=2022-04-03T23:17:37Z&se=2023-05-01T07:17:37Z&spr=https&sv=2020-08-04&sr=c&sig=wJkqOOZCPromubKaTzCAAY%2FvV5LJ7fIYHrbpwOJQDdk%3D"
container_client = ContainerClient.from_container_url(account_url)

file_names = []

#list files and generate cog
#rio cogeo create 
#rio-viz
for fp in glob.glob(local_path + "/*.tif"):
    #create cog
    #o = f.replace("/home/sachin/tmp/", "/home/sachin/tmp/cog/")
    #print("rio cogeo create " + f + " " + o)

    #file name
    fn = fp.replace(local_path + "/", "").strip()
    file_names.append(fn)
    #print(fn)
    
    #upload cog tiff
    #with open(fp, "rb") as blob_file:
    #    blob_name = "/".join(["mangroves", path.basename(fp)])
    #    container_client.upload_blob(name=blob_name, data=blob_file, overwrite=True)
    
#generate STAC mosiac json from cog urls
#https://deppcpublicstorage.blob.core.windows.net/output/mangroves/fsm_mangrove_2016.tif
#gdalinfo /vsicurl/https://deppcpublicstorage.blob.core.windows.net/output/mangroves/fsm_mangrove_2016.tif

year = "2016" 
mosaic = []
file_names = list(filter(lambda k: '_' + year in k, file_names))
for fn in file_names:
    print(fn)
    mosaic.append("https://deppcpublicstorage.blob.core.windows.net/output/mangroves/" + fn)

json_file = "pacific_mangroves_" + year + ".json"
mosaicdata = MosaicJSON.from_urls(mosaic)
with MosaicBackend(json_file, mosaic_def=mosaicdata) as mosaic:
    mosaic.write()

#upload mosiac json
with open(json_file, "rb") as blob_file:
        blob_name = "/".join(["mangroves", path.basename(json_file)])
        container_client.upload_blob(name=blob_name, data=blob_file)

print("Finished.")