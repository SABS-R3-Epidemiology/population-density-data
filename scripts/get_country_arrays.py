import rasterio
from rasterio import mask as msk
# import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import mapping


def get_country_arrays(tif_path, borders_path, out_path):

    tif_file = rasterio.open(tif_path)
    ghs_data = tif_file.read()

    ghs_data[0][ghs_data[0] < 0.0] = 0.0

    df = gpd.read_file(borders_path)

    canada = df.loc[df['ADMIN'] == 'Canada']
    uk = df.loc[df['ADMIN'] == 'United Kingdom']
    us = df.loc[df['ADMIN'] == 'United States of America']
    gib = df.loc[df['ADMIN'] == 'Gibraltar']
    ber = df.loc[df['ADMIN'] == 'Bermuda']

    # Mask
    can_array, clipped_transform = msk.mask(tif_file, [mapping(geom) for geom in canada.geometry.tolist()], crop=True)
    us_array, clipped_transform = msk.mask(tif_file, [mapping(geom) for geom in us.geometry.tolist()], crop=True)
    uk_array, clipped_transform = msk.mask(tif_file, [mapping(geom) for geom in uk.geometry.tolist()], crop=True)
    gib_array, clipped_transform = msk.mask(tif_file, [mapping(geom) for geom in gib.geometry.tolist()], crop=True)
    ber_array, clipped_transform = msk.mask(tif_file, [mapping(geom) for geom in ber.geometry.tolist()], crop=True)
    countries = {
        'Canada': can_array,
        'United Kingdom': uk_array,
        'United States of America': us_array,
        'Gibraltar': gib_array,
        'Bermuda': ber_array,
    }
    with open(out_path, 'wb') as f:
        np.savez_compressed(f, **countries)

get_country_arrays(snakemake.input[0], snakemake.input[1], snakemake.output[0])
