# import pandas as pd
import numpy as np
from affine import Affine


def lat_long_pops(countries_path, transforms_path, out_path):

    country_data = {}
    transform_data = {}

    with open(countries_path, 'rb') as f:
        npzfile = np.load(f)
        # for country in npzfile.files:
        for country in ['Bermuda']:
            country_data[country] = npzfile[country]

    with open(transforms_path, 'rb') as f:
        npzfile = np.load(f)
        # for country in npzfile.files:
        for country in ['Bermuda']:
            transform_data[country] = Affine.from_gdal(*npzfile[country])

    for country in country_data:
        transform = transform_data[country]
        csv_lines = 'latitude,longitude,population'
        for section in country_data[country]:
            for i in range(len(section)):
                for j in range(len(section[i])):
                    coords = transform * (i, j)
                    lat, long = coords
                    pop = section[i][j]
                    if pop > 0:
                        csv_lines += f'\n{lat},{long},{pop}'
        with open(f'data/processed/{country}.csv', 'w') as f:
            f.write(csv_lines)

lat_long_pops(snakemake.input[0], snakemake.input[1], snakemake.output[0])